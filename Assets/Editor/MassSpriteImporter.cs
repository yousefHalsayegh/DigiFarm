using UnityEngine;
using UnityEditor;
using UnityEditor.Animations;
using System.IO;
using System.Collections.Generic;

public class MassSpriteImporter : EditorWindow
{
    [System.Serializable]
    public class ActionSetup {
        public string actionName;
        public string frameIndicesString; // E.g. "0, 1" or "8, 9, 10, 11"
        public bool isLooping;

        public ActionSetup(string name, string frames, bool loop) {
            actionName = name; frameIndicesString = frames; isLooping = loop;
        }

        public int[] GetIndices() {
            List<int> idxList = new List<int>();
            string[] parts = frameIndicesString.Split(',');
            foreach (var p in parts) {
                if (int.TryParse(p.Trim(), out int val)) idxList.Add(val);
            }
            return idxList.ToArray();
        }
    }

    // Default Tamagotchi structure (Fully editable in the UI window)
    public List<ActionSetup> customActions = new List<ActionSetup>()
    {
        new ActionSetup("Hatching",   "0, 1, 2",     false),
        new ActionSetup("Idle",       "0, 1",        true),
        new ActionSetup("Walking",    "0, 1",        true),
        new ActionSetup("Eating",     "2, 3",        true),
        new ActionSetup("Sleeping_A", "4, 5",        true),
        new ActionSetup("Happy",      "3, 7",        true),
        new ActionSetup("Mad",        "6, 8",        true),
        new ActionSetup("Attacking",  "8, 11",false), 
        new ActionSetup("Sleeping_B", "10, 11",      true)
    };

    private float animationFPS = 2f;
    private string defaultStateName = "Walking";
    private Vector2 scrollPos;

    [MenuItem("Tools/Malleable Sprite & Anim Importer")]
    public static void ShowWindow()
    {
        GetWindow<MassSpriteImporter>("Malleable Importer");
    }

    private void OnGUI()
    {
        GUILayout.Label("Tamagotchi Animation Matrix Configurator", EditorStyles.boldLabel);
        animationFPS = EditorGUILayout.FloatField("Animation FPS", animationFPS);
        defaultStateName = EditorGUILayout.TextField("Default State Name", defaultStateName);
        
        GUILayout.Space(10);
        GUILayout.Label("Define Animation States & Frame IDs:", EditorStyles.miniBoldLabel);
        
        scrollPos = EditorGUILayout.BeginScrollView(scrollPos, GUILayout.Height(250));
        for (int i = 0; i < customActions.Count; i++)
        {
            EditorGUILayout.BeginHorizontal();
            customActions[i].actionName = EditorGUILayout.TextField(customActions[i].actionName, GUILayout.Width(120));
            customActions[i].frameIndicesString = EditorGUILayout.TextField(customActions[i].frameIndicesString);
            customActions[i].isLooping = EditorGUILayout.ToggleLeft("Loop", customActions[i].isLooping, GUILayout.Width(50));
            
            if (GUILayout.Button("X", GUILayout.Width(25))) {
                customActions.RemoveAt(i);
                break;
            }
            EditorGUILayout.EndHorizontal();
        }
        EditorGUILayout.EndScrollView();

        if (GUILayout.Button("+ Add Custom State")) {
            customActions.Add(new ActionSetup("NewState", "0, 1", true));
        }

        GUILayout.Space(15);
        if (GUILayout.Button("Batch Process & Mirror Folders", GUILayout.Height(40)))
        {
            ProcessSelected();
        }
    }

    private void ProcessSelected()
    {
        string[] selectedGuids = Selection.assetGUIDs;
        int count = 0;

        foreach (string guid in selectedGuids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            if (AssetDatabase.IsValidFolder(path))
            {
                string[] files = Directory.GetFiles(path, "*.*", SearchOption.AllDirectories);
                foreach (string file in files)
                {
                    if (file.EndsWith(".meta")) continue;
                    if (ExecutePipeline(file)) count++;
                }
            }
            else
            {
                if (!path.EndsWith(".meta") && ExecutePipeline(path)) count++;
            }
        }

        AssetDatabase.Refresh();
        EditorUtility.DisplayDialog("Pipeline Complete", $"Processed {count} items successfully.", "OK");
    }

    private bool ExecutePipeline(string path)
    {
        TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
        if (importer == null) return false;

        // Force slice layout configuration
        importer.textureType = TextureImporterType.Sprite;
        importer.spriteImportMode = SpriteImportMode.Multiple;
        importer.spritePixelsPerUnit = 16;
        importer.filterMode = FilterMode.Point;
        importer.textureCompression = TextureImporterCompression.Uncompressed;
        importer.isReadable = true;
        importer.SaveAndReimport();

        Texture2D texture = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        if (texture == null) return false;

        int sliceSize = 16;
        List<SpriteMetaData> metadata = new List<SpriteMetaData>();
        int idx = 0;

        for (int y = texture.height; y >= sliceSize; y -= sliceSize)
        {
            for (int x = 0; x < texture.width; x += sliceSize)
            {
                SpriteMetaData meta = new SpriteMetaData();
                meta.rect = new Rect(x, y - sliceSize, sliceSize, sliceSize);
                meta.alignment = (int)SpriteAlignment.Center;
                meta.name = texture.name + "_" + idx;
                metadata.Add(meta);
                idx++;
            }
        }
        importer.spritesheet = metadata.ToArray();
        importer.isReadable = false;
        importer.SaveAndReimport();

        // Target Folder Management
        string baseDir = Path.GetDirectoryName(path).Replace("\\", "/"); 
        string targetAnimDir = baseDir.Replace("Assets/Sprites", "Assets/Animations");
        if (targetAnimDir == baseDir) {
            targetAnimDir = Path.Combine("Assets/Animations", baseDir.Replace("Assets/", "")).Replace("\\", "/");
        }

        if (!Directory.Exists(targetAnimDir)) {
            Directory.CreateDirectory(targetAnimDir);
            AssetDatabase.Refresh();
        }

        Object[] subAssets = AssetDatabase.LoadAllAssetsAtPath(path);
        List<Sprite> sprites = new List<Sprite>();
        foreach (var sub in subAssets) { if (sub is Sprite s) sprites.Add(s); }
        if (sprites.Count == 0) return true;

        sprites.Sort((a, b) => {
            int aNum = int.Parse(a.name.Substring(a.name.LastIndexOf('_') + 1));
            int bNum = int.Parse(b.name.Substring(b.name.LastIndexOf('_') + 1));
            return aNum.CompareTo(bNum);
        });

        string filename = Path.GetFileNameWithoutExtension(path);

        // CREATE ANIMATOR CONTROLLER (Fixed index array reference mapping issue)
        string controllerPath = Path.Combine(targetAnimDir, filename + "_Animator.controller").Replace("\\", "/");
        AnimatorController controller = AnimatorController.CreateAnimatorControllerAtPath(controllerPath);
        AnimatorStateMachine stateMachine = controller.layers[0].stateMachine; // FIXED COMPILER ERROR

        AnimatorState defaultState = null;

        foreach (var template in customActions)
        {
            List<Sprite> clipFrames = new List<Sprite>();
            int[] frameIndices = template.GetIndices();
            
            foreach (int frameId in frameIndices)
            {
                if (frameId >= 0 && frameId < sprites.Count) {
                    clipFrames.Add(sprites[frameId]);
                }
            }

            if (clipFrames.Count > 0)
            {
                AnimationClip clip = CreateAnimationClip(targetAnimDir, filename + "_" + template.actionName, clipFrames, template.isLooping);
                AnimatorState newState = stateMachine.AddState(template.actionName);
                newState.motion = clip;

                if (template.actionName.ToLower() == defaultStateName.ToLower()) {
                    defaultState = newState;
                }
            }
        }

        if (defaultState != null) {
            stateMachine.defaultState = defaultState;
        }

        return true;
    }

    private AnimationClip CreateAnimationClip(string folder, string clipName, List<Sprite> frames, bool loops)
    {
        string animPath = Path.Combine(folder, clipName + ".anim").Replace("\\", "/");
        AnimationClip clip = new AnimationClip();
        
        if (loops) {
            AnimationClipSettings settings = AnimationUtility.GetAnimationClipSettings(clip);
            settings.loopTime = true;
            AnimationUtility.SetAnimationClipSettings(clip, settings);
        }

        EditorCurveBinding curveBinding = new EditorCurveBinding();
        curveBinding.type = typeof(SpriteRenderer);
        curveBinding.path = "";
        curveBinding.propertyName = "m_Sprite";

        ObjectReferenceKeyframe[] keyframes = new ObjectReferenceKeyframe[frames.Count];
        float frameTime = 1f / animationFPS; 

        for (int i = 0; i < frames.Count; i++) {
            keyframes[i] = new ObjectReferenceKeyframe();
            keyframes[i].time = i * frameTime;
            keyframes[i].value = frames[i];
        }

        AnimationUtility.SetObjectReferenceCurve(clip, curveBinding, keyframes);
        AssetDatabase.CreateAsset(clip, animPath);
        return clip;
    }
}
