abstract RPGChatbot = Numeral ** {
flags startcat = Command ;
cat
  Question ;
  Command ;
  Result ;
  Outcome ; 
  Enemy ;
  Item ;
  Location ;
  MoveDirection ;
  ProgramPrompt ;
  QuestionDirection ;
  Object ;
  Room ;
  RoomAdjective ;
  ItemAttribute ;
  ItemDescription ;
  EnemyAttribute ;
  EnemyPower ;
  Action ;
  Nouns ;

fun
  -- User actions

  -- what is <in front of me | behind me | on my left | on my right>
  QDirectionQuery : QuestionDirection -> Question ;
  -- what is in my backpack
  QItemQuery : Location -> Question ;
  -- what is around me
  QEntityQuery : Question ;
  -- Move forward, left, right, backwards.
  Move : MoveDirection -> Command ;
  -- Attack <enemy name> with <item name>.
  Attack : Enemy -> Item -> Command ;
  -- Attack same enemy as before with <item name>
  -- "attack with sharp sword"
  AttackSameTarget : Item -> Command ;
  -- Loot <enemy/object name>
  Loot : Object -> Command ;
  -- Move <item name> from <backpack> to <feet>
  MoveItem : Item -> Location -> Location -> Command ;
  -- Equip <item name>
  Equip : Item -> Command ;
  -- Unequip <item name>
  Unequip : Item -> Command ;
  -- Drop sharp sword
  Drop : Item -> Command ;
  -- Open treasure chest with magical key
  Open : Item -> Object -> Command ;
  -- Describe <enemy name>
  DescribeEnemy : Enemy -> Command ;
  -- Chatbot actions
  FightResult : Enemy -> Outcome -> Result ;
  -- There is a <door, enemy, chest, exit>
  ADirectionQuery : QuestionDirection -> Object ->  Result ;
  -- <Location> contains the items: <Python generated list>
  AItemQuery : Location -> Result ;
  -- "You moved forward"
  MoveSuccess : MoveDirection -> Result ;
  -- "You cannot go there, because there is a boulder"
  MoveFail : Object -> Result ;
  -- "You put viking helmet to head"
  ItemMoveSuccess : Item -> Location -> Result ;
  -- "You cannot put sword there"
  ItemMoveFail : Item -> Result ;
  -- "You can't equip <item name>"
  EquipFail : Item -> Result ;
  -- "<item name> was not equipped."
  UnequipFail : Item -> Result ; 
  -- "head has viking helmet already"
  ItemSlotTaken : Item -> Location -> Result ;
  -- "You hit the depressed goblin and they lost 10 health"
  AttackSuccess : Enemy -> Digits -> Result ;
  -- "The goblin hit you and you lost 10 health"
  EnemyAttack : Enemy -> Digits -> Result ;
  -- "You have 10 health left."
  PlayerHealth : Digits -> Result ;
  -- "The angry goblin has 15 health left"
  EnemyHealth : Enemy -> Digits -> Result ; 
  PlayerDeath : Result ;
  -- Old tiger|door doesn't exist.
  ObjectMissing : Object -> Result ;
  -- Telling that object is locked.
  ObjectLocked : Object -> Result ;
  -- Telling that object has been opened.
  ObjectUnlocked : Object -> Result ;
  -- Telling that object cannot be opened.
  ObjectInvalidUnlock : Object -> Result ;
  -- Telling that object cannot be looted.
  ObjectInvalidLoot : Object -> Result ;
  -- You found a dull axe.
  LootSuccess : Item -> Result ;
  -- You can't loot that because it is alive.
  LootEnemyFail : Result ;
  -- Telling that enemy is weak/strong against some item attribute and that they have some specific item.
  EnemyDescWithItem : Enemy -> EnemyAttribute -> ItemDescription -> Item -> Result ;
  -- Telling that enemy is weak/strong against some item attribute and that they have some specific item.
  EnemyDescWithoutItem : Enemy -> EnemyAttribute -> ItemDescription -> Result ;
  -- There is an angry dragon with shiny sword.
  EnemyEncountered : Enemy -> Item -> Result ;
  -- You arrive into a room <number>.
  RoomIntro : Room -> RoomAdjective -> Result ;
  -- Used to prompt user for input in the program.
  InputPrompt : ProgramPrompt ;
  -- Used to prompt user for attack command in battle.
  BattlePrompt : ProgramPrompt ;
  -- Used to tell user that they are already fighting one enemy.
  BattleInvalidTarget : Enemy -> Result ;
  -- Used to tell the user that the action is not valid.
  InvalidAction : Result ;
  -- Telling that item does not exist.
  ItemMissing : Item -> Result ;
  
  -- Lexicon
  -- Shiny sword, Dull axe, Sharp bread
  ItemMod : ItemAttribute -> Item -> Item ;
  -- Shiny items, Dull items
  ItemType : ItemAttribute -> ItemDescription ;
  Sharp, Dull, Broken, Legendary, Magical, Shiny, Fiery, Mysterious, Frozen : ItemAttribute ;
  Sword, Axe, Hammer, WizardStaff, Key, ScottishKilt, LeatherSkirt, VikingHelmet, BaseballCap, UndyingTotem : Item;
  -- Angry dragon, Nice mouse
  EnemyMod : EnemyAttribute -> Enemy -> Enemy ;
  Angry, Happy, Furious, Old, Weak, Strong : EnemyAttribute ;

  Orc, Goblin, Dragon, Bandit, Mouse, Tiger, Minotaur : Enemy;

  -- Objects that can exist in some direction.
  -- "There is a door"
  Door, Chest, Boulder, Exit, Gate, Bag, Wall, PileOfBones : Object ;
  EnemyObject : Enemy -> Object ;
  -- Locations of where items can be put
  Backpack, Head, Legs : Location ;

  -- "... and it is damp"
  Damp, Bright, Dark, Creepy, Scary, Peaceful : RoomAdjective ;

  Forward, Backward, Left, Right : MoveDirection ;
  Infront, Behind, LeftSide, RightSide : QuestionDirection ;

  -- Verbs used for fight outcome.
  Win, Lose : Outcome ;

  -- Helper verbs
  loot_V2, drop_V2, describe_V2, attack_V2, equip_V2, unequip_V2, move_V2, lock_V2, search_V2, unlock_V2 : Action ;
  health_N, action_N, inventory_N : Nouns ;
  -- Used for creating numbered rooms such as "Room 15"
  RoomNumber : Int -> Room ;
  
}
