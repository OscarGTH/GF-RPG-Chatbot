abstract RPGChatbot = {
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
  QuestionDirection ;
  Object ;
  RoomAdjective ;
  ItemList ;
  ItemAttribute ;
  EnemyAttribute ;
  EnemyPower ;

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
  Loot : Enemy -> Command ;
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
  AWhatItemsAreIn : Location -> ItemList -> Result ;
  APut : Item -> Location -> Result ;
  -- Depressed shark doesn't exist.
  EnemyMissing : Enemy -> Result ;
  -- You find dull axe.
  LootSuccess : Item -> Result ;
  -- You arrive into a room <number>.
  RoomIntro : Int -> Result ;
  -- Room is damp.
  RoomDescription : RoomAdjective -> Result ;
  -- Dragon is weak against sharp items.
  EnemyDescription : Enemy -> EnemyPower -> ItemAttribute -> Result ;
  -- There is an angry dragon with shiny sword.
  EnemyEncountered : Enemy -> Item -> Result ;
  -- Lexicon
  -- Shiny sword, Dull axe, Sharp bread
  ItemMod : ItemAttribute -> Item -> Item ;
  Sharp, Dull, Shiny, Fiery, Mysterious, Frozen : ItemAttribute ;
  Sword, Axe, Book, Bread, Ring, Knife, Hammer, Key : Item;
  
  -- Angry dragon, Nice mouse
  EnemyMod : EnemyAttribute -> Enemy -> Enemy ;
  Angry, Happy, Depressed : EnemyAttribute ;

  Orc, Goblin, Dragon, Snake, Mouse, Tiger, Shark : Enemy;

  -- There is a dragon on the left.
  EnemyObject : Enemy -> Object ;

  -- Objects that can exist in some direction.
  -- There is a door in front of you.
  Door, Chest, Rock, Exit, Gate : Object ;

  Pockets, Backpack, Head, Feet, Hands, Pants : Location ;
  Damp, Bright, Dark, Dim : RoomAdjective ;
  Forward, Backward, Left, Right : MoveDirection ;
  Infront, Behind, LeftSide, RightSide : QuestionDirection ;
  Win, Lose : Outcome ;
  WeakAgainst, StrongAgainst : EnemyPower ;
  
}
