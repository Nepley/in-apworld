# Touhou 8 ~ Imperishable Night Apworld

This is an implementation of touhou 8 for [Archipelago](https://github.com/ArchipelagoMW/Archipelago)<br />

## How does this randomizer work ?
At the start, you start with only one team (or all solo characters if they are enabled), with zero resources and with only the Lunatic difficulty.<br />
Each item will make it easier and easier to clear the differents stages.
If Spell Practice is enabled, you will need to complete each individual spellcard with each team/character.

## Locations
* MidBoss Defeated
* Boss Defeated
* Stage Cleared
* Time requirement
* SpellCard in Spell Practice

## Items
* Teams
* Next Stage (Practice Mode)
* Extra Stage (If enabled)
* Pack of 25 Power Points
* Pack of 1000 Time Points
* Lives
* Bombs
* Lower Difficulty
* SpellCards (With Spell Practice)
* Being able to collect time (If enabled)

### Filler: 
* 1 Power Point
* 10 Time Points
* 50 Time Points

## Options

### Global Options

**Mode:** Practice/Normal mode and/or Spell Practice.<br />
In Practice mode, you play stage by stage individually and need to unlock the stages.<br />
In Normal mode, you need to finish the game normally with the resources only given at the start. Futhermore, only the resources act as a gate. If you put everything at minimum in the yaml, the logic consider you can finish at sphere 1.<br />
In Spell Practice, you will need to unlock and complete individual spellcard, granting one check per team/character

**Characters:** Choose If you want to play with the 4 teams and/or the 8 solo characters. Due to limitations, solo characters will all be unlocked from the start if they are enabled and their Extra Stage unlock is grouped.

**Goal:** Depending if the extra stage and/or spell practice is enabled, you can choose which goal you want between Eirin, Kaguya, Mokou, the three of them, if you need to get all Kaguya's treasure or if you need to complete a set number of spellcard.

**Death Link:** You can choose to activate Death Link. You can also change if it's triggered by losing a life or getting a game over. And you can set an amnesty before it send a death to others. Can be changed at any time on the client.

**Ring Link:** You can choose to activate Ring Link, synchronizing your gain and loss of Power Points. Can be changed at any time on the client.

### Normal/Practice Mode Options

**Stage Unlock:** In Practice only, Stages can be unlocked gobally or per team/character.

**Progressive Stage:** In Practice only, you can choose if you want the stages to be unlocked progressively or not.

**Exclude Lunatic:** You can exclude the Lunatic difficulty and therefore, start with the Hard difficulty.

**Resources:** You can set the resources needed for the stages 3/4ab, stages 5/6ab and extra stage if enabled.

**Extra Stage:** You can enable the extra stage and choose if it act as the 7th stage or if it is unlocked separately. In normal mode, it is unlocked after clearing the stage 6A or 6B if it's not it's own unlock.

**Time Check:** Determine if time requirement in the first 5 stages are locations.

**Time:** Choose if the ability to gain time is locked behind an item.

**Both Stage 4:** In Practice only, you can choose if each team/character will have both stage 4A and 4B or only the one the normally have.

**Endings Required:** If the goal is set to one of the bosses, set if you must clear your goal with just one team/character or all of them.

**Difficulty:** If checks are separated by difficulty. If Lunatic is excluded, no check will be behind it. An option also allow to complete easier (and unlocked) difficulty when doing an harder one.

**Traps:** You can choose to have traps replacing a percentages of filler items. You can set the weight of each individual trap.

**Limit Lives/Bombs:** You can set a limit to your maximum number if lives/bombs in-game/ It doesn't remove any lives/bombs from the rando, but will do nothing once the maximum is reach. Can be changed at any time on the client.

### Spell Practice Options

**SpellCard Teams**: Choose how many team will have to do the spellcards.

**Starting SpellCard Count:** Determine the number of spellcard you start with.

**Max SpellCard Count:** Choose the maximal number of spellcard that will exist int the randomizer

**SpellCard Difficulties / Stages:** Filter spellcards based on their stage and difficulty.

**Duplicate SpellCards:** Set a percentage of filler item that will be replace by duplicate item to unlock spellcards.

**Exclude/Include SpellCards:** Choose which spellcard you want to exclude or force it's inclusion in the randomizer.

**Treasure Location:** If the goal is set to "Kaguya's Treasure", choose where they are located.

**Treasure Final SpellCard:** If the goal is set to "Kaguya's Treasure", choose which spellcard will be unlocked once all treasure are collected and need to be cleared to goal.

**Capture SpellCards Count:** If the goal is set to "Capture SpellCards", choose how many spellcards is necessary to be cleared.

**Capture SpellCards Stage:** If the goal is set to "Capture SpellCards", choose which spellcards, grouped by stage, count toward the goal.

## How to use

**Backup your score.dat if you care about your scores, practice stage access spell practice access and Extra unlock**

1. Launch the game
2. Launch and connect the client "Touhou IN" found in the archipelago launcher to the server.
3. If the message "Touhou IN process found. Starting loop..." appeared, you're good to go