# Python Text Effects for Blender

Define data describing individual text effects and use those effects to automatically keyframe letter-by-letter transforms in your animated scene.

## Getting Started

I think the info from my [Blender customizations repo](https://github.com/Botmasher/blender-vse-customizations) still applies here, but fill out this startup guide with specifics.

## Background

I've used Blender to animate text objects in dozens and dozens of animation projects. It lacks the kind of stock text effects familiar to 3D text and NLE applications, but I tended to resorted to doing complex text effects by hand, often rolling the visuals into less demanding but less impressive word or sentence-level animations.

I looked into automating this process, and one of the immediate challenges that stood out to me were: (1) automatically keyframing letter-by-letter animations, (2) shaping different effects and applying them consistently, (3) balancing user customization vs predetermined properties for distinct effects, and (4) allowing modification or stacking of effects. Two more challenges showed up in my early experiments: (5) juggling user input properties and (6) persisting data between sessions to remember and update individual created text effects.

Comparing my amateur video-editing experience to my animation routine, I decided to tackle these six problems and work towards a tool that could apply text effects. This script grew from my [Blender scripting projects](https://github.com/Botmasher/blender-vse-customizations) and now aims to be a fully functioning add on.

## Behavior

Describe what the program accomplishes, the main problems it solves, and how it does. Comment with the reasoning and intended behavior.

## Source code

The code lives in a single `source.py` file. As I work through the code, I'll encapsulate and pull it out into coherent files. Once that's done, return here and give an overview of the code.
