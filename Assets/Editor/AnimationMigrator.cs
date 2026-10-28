using UnityEngine;
using UnityEditor;
using System.IO;
using System.Collections.Generic;

public class RobustBatchLinker : EditorWindow
{
    private string animationsRootPath = "Assets/Animations";
    private RuntimeAnimatorController masterDigitama;
    private RuntimeAnimatorController masterDigimon;

    [MenuItem("Tools/Complete Auto-Sort & Link System")]
    public static void ShowWindow()
    {
        GetWindow<RobustBatchLinker>("Auto-Sort & Linker");
    }

    private void OnGUI()
    {
        GUILayout.Label("Tamagotchi Subspecies Folder Creator & Linker", EditorStyles.boldLabel);
        GUILayout.Space(10);

        animationsRootPath = EditorGUILayout.TextField("Animations Root Path", animationsRootPath);
        masterDigitama = (RuntimeAnimatorController)EditorGUILayout.ObjectField("Master Digitama Controller", masterDigitama, typeof(RuntimeAnimatorController), false);
        masterDigimon = (RuntimeAnimatorController)EditorGUILayout.ObjectField("Master Digimon Controller", masterDigimon, typeof(RuntimeAnimatorController), false);

        GUILayout.Space(15);
        EditorGUILayout.HelpBox(
            "HOW THIS WORKS:\n" +
            "1. Scans ALL animations inside your folder recursively.\n" +
            "2. Groups them by their EXACT prefix name (handles Agumon vs Agumon_Black).\n" +
            "3. CREATES missing subfolders automatically on your hard drive.\n" +
            "4. Moves your files there and builds the clean Override Controllers.", 
            MessageType.Info
        );

        GUILayout.Space(10);
        if (GUILayout.Button("Run Full Auto-Sort & Linking", GUILayout.Height(40)))
        {
            if (masterDigitama == null || masterDigimon == null)
            {
                EditorUtility.DisplayDialog("Error", "Please assign both Master Controllers first!", "OK");
                return;
            }
            ExecuteFullPipeline();
        }
    }

    private void ExecuteFullPipeline()
    {
        if (!Directory.Exists(animationsRootPath))
        {
            EditorUtility.DisplayDialog("Error", $"Path {animationsRootPath} missing!", "OK");
            return;
        }

        // 1. Discover all animation clips anywhere inside the target directory
        string[] animGuids = AssetDatabase.FindAssets("t:AnimationClip", new[] { animationsRootPath });
        Dictionary<string, List<AnimationClip>> creatureGroups = new Dictionary<string, List<AnimationClip>>();

        foreach (string guid in animGuids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            AnimationClip clip = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);
            if (clip == null) continue;

            string filename = Path.GetFileNameWithoutExtension(path);
            
            // Extract the precise creature/subspecies prefix string identifier
            // Handles extracting "Agumon" or "Agumon_Black" by splitting at the action suffixes
            string prefix = ExtractCreaturePrefix(filename);
            if (string.IsNullOrEmpty(prefix)) continue;

            if (!creatureGroups.ContainsKey(prefix))
            {
                creatureGroups[prefix] = new List<AnimationClip>();
            }
            creatureGroups[prefix].Add(clip);
        }

        int folderCount = 0;

        // 2. Process each detected unique prefix group
        foreach (var group in creatureGroups)
        {
            string creatureName = group.Key;
            List<AnimationClip> clips = group.Value;

            // Define target folder path natively inside Assets
            string targetFolder = Path.Combine(animationsRootPath, creatureName).Replace("\\", "/");
            
            // AUTOMATIC FOLDER CREATION: Build physical directories if missing
            if (!Directory.Exists(targetFolder))
            {
                Directory.CreateDirectory(targetFolder);
                AssetDatabase.Refresh();
            }

            // Move the loose files cleanly into their respective target folder location
            List<AnimationClip> movedClips = new List<AnimationClip>();
            foreach (var clip in clips)
            {
                string oldPath = AssetDatabase.GetAssetPath(clip);
                string newPath = Path.Combine(targetFolder, Path.GetFileName(oldPath)).Replace("\\", "/");
                
                if (oldPath != newPath)
                {
                    string error = AssetDatabase.MoveAsset(oldPath, newPath);
                    if (string.IsNullOrEmpty(error))
                    {
                        // Reload asset at the new valid path location loop reference tracking
                        AnimationClip movedClip = AssetDatabase.LoadAssetAtPath<AnimationClip>(newPath);
                        if (movedClip != null) movedClips.Add(movedClip);
                    }
                    else
                    {
                        movedClips.Add(clip); // Fallback reference tracking
                    }
                }
                else
                {
                    movedClips.Add(clip);
                }
            }

            // Determine if this is an Egg or general pet structure tracking
            bool isDigitama = creatureName.ToLower().Contains("digitama");
            RuntimeAnimatorController targetedMaster = isDigitama ? masterDigitama : masterDigimon;

            // Generate clean target override files
            string overridePath = Path.Combine(targetFolder, creatureName + "_Override.overrideController").Replace("\\", "/");
            AnimatorOverrideController overrideController = AssetDatabase.LoadAssetAtPath<AnimatorOverrideController>(overridePath);

            if (overrideController == null)
            {
                overrideController = new AnimatorOverrideController();
                AssetDatabase.CreateAsset(overrideController, overridePath);
            }

            overrideController.runtimeAnimatorController = targetedMaster;

            // Map animation tracks safely into layout array blocks
            var clipOverrides = new List<KeyValuePair<AnimationClip, AnimationClip>>(overrideController.overridesCount);
            overrideController.GetOverrides(clipOverrides);

            for (int i = 0; i < clipOverrides.Count; i++)
            {
                string masterStateName = clipOverrides[i].Key.name.ToLower();

                AnimationClip localMatch = movedClips.Find(clip => {
                    string clipNameLower = clip.name.ToLower();
                    if (clipNameLower.EndsWith("_" + masterStateName)) return true;
                    if (clipNameLower == masterStateName) return true;
                    
                    string cutMasterState = masterStateName.Replace("ing", "");
                    if (clipNameLower.Contains(cutMasterState)) return true;
                    return false;
                });

                if (localMatch != null)
                {
                    clipOverrides[i] = new KeyValuePair<AnimationClip, AnimationClip>(clipOverrides[i].Key, localMatch);
                }
            }

            overrideController.ApplyOverrides(clipOverrides);
            EditorUtility.SetDirty(overrideController);
            folderCount++;
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
        EditorUtility.DisplayDialog("Pipeline Complete", $"Successfully sorted files and created {folderCount} subspecies folder systems!", "OK");
    }

    private string ExtractCreaturePrefix(string filename)
    {
        // Strict list of common core Tamagotchi action name arrays
        string[] actions = { "_Walking", "_Eating", "_Happy", "_Mad", "_Sleeping", "_Tired", "_Attacking", "_Hatching", "_Hatch" };
        string filenameLower = filename.ToLower();

        foreach (string action in actions)
        {
            int idx = filenameLower.LastIndexOf(action);
            if (idx > 0)
            {
                // Returns "Agumon" or "Agumon_Black" directly by stripping the action off the tail end cleanly!
                return filename.Substring(0, idx);
            }
        }

        // Alternative split indexer fallback if file layout properties use standard underscores
        int simpleSplit = filename.LastIndexOf('_');
        if (simpleSplit > 0) return filename.Substring(0, simpleSplit);

        return filename; 
    }
}
