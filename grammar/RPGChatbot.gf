abstract RPGChatbot = Numeral ** {
flags startcat = Command ;
cat
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

  -- what is <in front of me | behind me | on the left of me | on the right of me>
  QDirectionQuery : QuestionDirection -> Command ;
  -- what is in my backpack
  QItemQuery : Location -> Command ;
  -- what is in this room
  QEntityQuery : Nouns -> Command ;
  -- Move forward, left, right, backward.
  Move : MoveDirection -> Command ;
  -- Attack <enemy name> with <item name>.
  Attack : Enemy -> Item -> Command ;
  -- Attack same enemy as before with <item name>
  -- "attack with sharp sword"
  AttackSameTarget : Item -> Command ;
  -- Loot <enemy/object name>
  Loot : Object -> Command ;
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
  -- Notifying that item has been dropped.
  DropSuccess : Item -> Result ;
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
  -- "You hit the infernal goblin and they lost 10 health"
  AttackSuccess : Enemy -> Digits -> Result ;
  -- "There is nothing to attack"
  AttackFail : Result ;
  -- "The goblin hit you and you lost 10 health"
  EnemyAttack : Enemy -> Digits -> Result ;
  -- "You have 10 health left."
  PlayerHealth : Digits -> Result ;
  -- "The weak goblin has 15 health left"
  EnemyHealth : Enemy -> Digits -> Result ;
  -- "You died"
  PlayerDeath : Result ;
  -- "You used <item>"
  ItemUse : Item -> Result ;
  -- "You recovered <digits> health"
  HealthRecover : Digits -> Result ;
  -- goblin|door doesn't exist.
  ObjectMissing : Object -> Result ;
  -- Telling that object is locked.
  ObjectLocked : Object -> Result ;
  -- Telling that object has been opened.
  ObjectUnlocked : Object -> Result ;
  -- Telling that object cannot be opened.
  ObjectInvalidUnlock : Object -> Result ;
  -- Telling that item cannot be used for opening.
  InvalidUnlockItem : Item -> Result ;
  -- Telling that object cannot be looted.
  ObjectInvalidLoot : Object -> Result ;
  -- You found a dull axe.
  LootSuccess : Item -> Result ;
  -- You can't loot that because it is alive.
  LootEnemyFail : Result ;
  -- Telling that enemy is weak/strong against some item attribute and that they have some specific item.
  EnemyDescWithItem : Enemy -> EnemyAttribute -> ItemDescription -> Item -> Result ;
  -- Telling that enemy is weak/strong against some item attribute.
  EnemyDescWithoutItem : Enemy -> EnemyAttribute -> ItemDescription -> Result ;
  -- There is an infernal dragon with shiny sword.
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
  -- Used to tell that command is not understood.
  InvalidInput : Result ;
  -- Telling that item does not exist.
  ItemMissing : Item -> Result ;
  
  -- Lexicon
  -- Shiny sword, Dull axe, Magical hammer
  ItemMod : ItemAttribute -> Item -> Item ;
  -- Shiny items, Dull items
  ItemType : ItemAttribute -> ItemDescription ;
  Sharp, Dull, Broken, Legendary, Magical, Shiny, Fiery, Mysterious, Frozen : ItemAttribute ;
  Sword, Axe, Hammer, WizardStaff, Key, PlatiniumSkirt, LeatherSkirt, VikingHelmet, BaseballCap, UndyingTotem : Item;
  -- Veteran demon, infernal orc
  EnemyMod : EnemyAttribute -> Enemy -> Enemy ;
  Infernal, Veteran, Young, Rabid, Beefy, Weak, Strong : EnemyAttribute ;

  Troll, Goblin, Dragon, GiantRat, Ghoul, Demon, Skeleton, Wizard : Enemy;

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

  -- Used for creating numbered rooms such as "Room 15"
  RoomNumber : Int -> Room ;

}
