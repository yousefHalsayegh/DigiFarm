# DigiFarm

**Adaptive Digital-Creature Simulation**  
**Personal Project | Python 3.12, Pygame, NLP, Reinforcement Learning**

DigiFarm is a personal Python/Pygame project inspired by virtual-pet games and the Digimon franchise. It combines creature raising, resource-management ideas, semantic-analysis-driven evolution, persistent game state, and an early AI system intended to support future reinforcement-learning experiments.

The current implementation focuses on raising and evolving digital creatures, while the longer-term design is intended to move toward a deeper simulation experience influenced by both **Tamagotchi-style virtual pets** and **Dwarf Fortress-style management systems**.

> **Project status:** Paused. The current repository reflects an earlier stage of the project and of my development experience, with several systems working and others left as future extensions.

## Overview

The project is built as a desktop game/application using **Python**, **Pygame**, and **Pygame GUI**.

The main entry point, `start.py`, launches a graphical menu with:

- **New Game**
- **Continue**
- **Settings**
- **Exit**

The game stores persistent state in JSON-backed save data. Saved information includes the wider game state, locations, and monster information.

A key experiment in DigiFarm is the use of **semantic analysis as part of monster growth and evolution**. This creates a path toward creatures whose development is influenced by interpreted input rather than only fixed stat thresholds.

## Current Features

Implemented or currently functional systems include:

- Creature raising
- Monster growth and evolution
- Semantic-analysis-driven evolution logic
- Save and load functionality
- Persistent game state
- Location and monster data storage
- Simple AI behaviour
- Simple tile editor
- Menu and screen navigation
- JSON-based data
- Custom Pygame GUI styling

## Gameplay Direction

The current gameplay is centred on **raising monsters**.

The broader design goal is a simulation that combines:

- the personal attachment and progression of a virtual-pet game;
- the creature-evolution concept associated with Digimon-inspired games;
- deeper management systems inspired by simulation games such as *Dwarf Fortress*.

The project is not intended to be a direct recreation of either game. They are design inspirations for a more systems-driven creature simulation.

## Semantic Analysis and Evolution

Semantic analysis is part of DigiFarm's creature growth and evolution system.

Rather than treating evolution only as a fixed sequence of hard-coded conditions, the project experiments with semantic information as an input to how a creature develops.

This system is one of the foundations for a longer-term goal: giving each monster a more independent decision-making model and eventually introducing reinforcement learning into creature behaviour.

## Save System

The save/load system is functional and stores the game state needed to continue a session, including:

- monster information;
- locations;
- broader game-state data.

Save data is stored in JSON-based files under the project's data structure.

## Controls

The current implementation is primarily **keyboard controlled**.

Mouse interaction is planned for future versions as the management and interface systems become more complex.

## Tech Stack

- Python 3.12
- Pygame
- Pygame GUI
- JSON
- Semantic / NLP-based analysis
- Early AI systems
- Reinforcement learning *(planned extension)*

> The repository currently uses additional Python dependencies beyond `pygame` and `pygame_gui`. A complete dependency file has not yet been added.

## Project Structure

```text
DigiFarm/
├── Assests/
│   └── style/
├── Screens/
├── Systems/
├── digi/
├── save_data/
├── screens/
├── systems/
├── start.py
└── training.py
```

### Notes on the current structure

- `digi/` is related to the Conda environment/package setup rather than a core gameplay module.
- The repository currently contains similarly named directories with different capitalization, including `Screens` / `screens` and `Systems` / `systems`.
- These duplicated directory names are legacy project structure that should be cleaned up.
- `training.py` is currently only a testing utility and is **not** the reinforcement-learning training implementation.

## Installation

The project has currently been tested on **Windows** with **Python 3.12**.

Clone the repository:

```bash
git clone https://github.com/yousefHalsayegh/DigiFarm.git
cd DigiFarm
```

The repository currently does not provide a complete `requirements.txt` or `pyproject.toml`, so the full environment is not yet reproducible from a single dependency command.

At minimum, the graphical interface depends on:

```bash
pip install pygame pygame_gui
```

Additional dependencies are used elsewhere in the project.

## Running the Project

```bash
python start.py
```

This opens the DigiFarm main menu in a Pygame window.

## Current Limitations

DigiFarm is an unfinished personal project and currently has several limitations:

- the project structure needs cleanup;
- dependency management is incomplete;
- some gameplay and management systems are still basic;
- the Settings flow is incomplete;
- the AI system is still simple;
- the planned reinforcement-learning system for individual monsters has not yet been implemented;
- there are currently no project screenshots or gameplay GIFs in the repository.

## Planned Development

If development resumes, the intended areas of expansion are:

- reinforcement-learning behaviour for individual monsters;
- a simple higher-level control system;
- deeper management mechanics;
- improved creature logic;
- a better map system;
- increased mouse-driven interaction;
- cleaner project/package structure.

## Project Context

DigiFarm is a **personal passion project** and was written as an original project rather than as a fork or tutorial implementation.

The project was motivated by the idea of building a systems-driven virtual-creature simulation inspired by the Digimon franchise while exploring game-state architecture, persistent data, semantic analysis, AI behaviour, and eventually reinforcement learning.

Because the repository comes from an earlier stage of my programming experience, some architectural and organisational choices remain rough. I have kept the project available as part of my portfolio because it shows the progression from conventional game logic toward more adaptive creature behaviour and learning-based systems.

## License

No license is currently specified for this repository.
