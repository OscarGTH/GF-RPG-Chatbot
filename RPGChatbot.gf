abstract RPGChatbot = {
flags startcat = Command ;
cat
  Question ;
  Command ;
  Result ;
  Narrative ;
  Outcome ; 
  Enemy ;
  Item ;
  Location ;
  MoveDirection ;
  QuestionDirection ;
  Object ;
  Room ;
  RoomAdjective ;
  ItemList ;
  ItemAttribute ;
  ItemDescription ;
  EnemyAttribute ;
  EnemyPower ;
  Action ;

fun
  -- User actions

  -- What is <in front of me | behind me | on my left | on my right | in my backpack>
  QWhatIsInDirection : QuestionDirection -> Question ;
  QWhichItemsAreIn : Location -> Question ;
  -- Move forward, left, right, backwards.
  Move : MoveDirection -> Command ;
  -- Attack <enemy name> with <item name>.
  Attack : Enemy -> Item -> Command ;
  -- Loot <enemy name>
  Loot : Object -> Command ;
  -- Put <item name> <into backpack | onto body parts>
  Put : Item -> Location -> Command ;
  -- Drop sharp sword
  Drop : Item -> Command ;
  -- Describe <enemy name>
  DescribeEnemy : Enemy -> Command ;
  -- Chatbot actions
  FightResult : Enemy -> Outcome -> Result ;
  -- There is a <door, enemy, chest, exit>
  AWhatIsInDirection : Object -> Result ;
  -- <Location> contains <list of items>
  AWhichItemsAreIn : Location -> ItemList -> Result ;
  APut : Item -> Location -> Result ;
  -- Depressed shark doesn't exist.
  EnemyMissing : Enemy -> Result ;
  -- You found a dull axe.
  LootSuccess : Item -> Result ;
  -- You arrive into a room <number>.
  RoomIntro : Room -> RoomAdjective -> Narrative ;
  -- Room is damp.
  RoomDescription : RoomAdjective -> Result ;
  -- Dragon is weak against sharp items.
  EnemyDescription : Enemy -> EnemyPower -> ItemDescription -> Result ;
  -- There is an angry dragon with shiny sword.
  EnemyEncountered : Enemy -> Item -> Result ;
  
  -- Lexicon
  -- Shiny sword, Dull axe, Sharp bread
  ItemMod : ItemAttribute -> Item -> Item ;
  -- Shiny items, Dull items
  ItemType : ItemAttribute -> ItemDescription ;
  Sharp, Dull, Shiny, Fiery, Mysterious, Frozen : ItemAttribute ;
  Sword, Axe, Book, Bread, Ring, Knife, Hammer, Key : Item;
  
  -- Angry dragon, Nice mouse
  EnemyMod : EnemyAttribute -> Enemy -> Enemy ;
  Angry, Happy, Depressed : EnemyAttribute ;

  Orc, Goblin, Dragon, Bandit, Mouse, Tiger, Minotaur : Enemy;

  -- "There is a dragon on the left."
  EnemyObject : Enemy -> Object ;

  -- Objects that can exist in some direction.
  -- "There is a door"
  Door, Chest, Boulder, Exit, Gate, Bag, Wall : Object ;

  -- Locations of where items can be put
  Pockets, Backpack, Head, Feet, Hands, Pants : Location ;

  -- "... and it is damp"
  Damp, Bright, Dark, Creepy, Scary, Peaceful : RoomAdjective ;

  Forward, Backward, Left, Right : MoveDirection ;
  Infront, Behind, LeftSide, RightSide : QuestionDirection ;

  -- Verbs used for fight outcome.
  Win, Lose : Outcome ;

  -- Enemies can be either strong or weak against something.
  Weak, Strong : EnemyPower ;

  -- Helper verbs
  find_V2, loot_V2, drop_V2, put_V2, describe_V2, attack_V2, move_V2, search_V2 : Action ;

  -- Used for creating numbered rooms such as "Room 15"
  RoomNumber : Int -> Room ;
  
}
