concrete RPGChatbotEng of RPGChatbot = open
  Prelude,
  SymbolicEng,
  SymbolEng,
  SyntaxEng,
  ParadigmsEng,
  IdiomEng,
  QuestionEng in {

lincat
  Command = Imp ;
  Question = Utt ;
  Result = Utt ;
  Narrative = Utt ;
  Outcome = V2 ;
  Enemy = CN ;
  EnemyAttribute = A ;
  EnemyPower = A2 ;
  ItemDesc = NP ;
  Room = NP ;
  Item = CN ;
  ItemAttribute = A ;
  MoveDirection = NP ;
  RoomAdjective = A ;
  Object = CN ;
  QuestionDirection = Prep ;
  Location = Adv ;
  Action = V2 ;

lin
  -- [ COMMANDS ]
  -- Moving character
  Move dir =
    mkImp move_V2 dir;
  -- TODO: Add item that is attacked with or use the weapon in hands.
  Attack enemy item = 
    mkImp attack_V2 (mkNP the_Det enemy) ;
  -- Looting enemies
  Loot enemy =
    mkImp loot_V2 (mkNP the_Det enemy)
    | mkImp search_V2 (mkNP the_Det enemy) ;
  Drop item =
    mkImp drop_V2 (mkNP the_Det item) ;
  -- TODO: Add location of where to put item to.
  Put item location =
    mkImp put_V2 (mkNP the_Det item) ;
  DescribeEnemy enemy =
    mkImp describe_V2 (mkNP the_Det enemy) ;


  -- [ QUESTIONS ]
  QWhatIsInDirection direction =
    mkUtt (mkQCl what_IP (SyntaxEng.mkAdv direction i_NP)) ;
  QWhichItemsAreIn location =
    mkUtt (mkQCl (mkIP whichPl_IDet (mkN "item")) location) ;

  --[CHATBOT ANSWERS]
  -- Finding items as a result of looting
  LootSuccess item =
    mkUtt (mkS pastTense (mkCl you_NP find_V2 (mkNP a_Det item))) ;
  -- Telling that enemy doesn't exist.
  EnemyMissing enemy = mkUtt (mkS negativePol (mkCl (mkNP enemy) (mkV "exist"))) ;
  -- Telling that enemy has been encountered.
  EnemyEncountered enemy item = 
    mkUtt (mkCl (mkCN enemy (SyntaxEng.mkAdv with_Prep (mkNP a_Det item)))) ;
  -- Telling what is in the direction.
  AWhatIsInDirection object =
    mkUtt (mkCl object) ;
  -- Outcome of the fight (Whether enemy won or lost.)
  FightResult enemy outcome =
    mkUtt (mkS pastTense (mkCl (mkNP the_Det enemy) outcome (mkNP the_Det (mkN "fight")))) ;
  -- Intro phrase when arriving to a new room. In the form of "You arrived into room <number> and it is <adjective>".
  RoomIntro room adj =
    mkUtt (mkS and_Conj (mkS pastTense (mkCl you_NP (mkV2 (mkV "arrive") to_Prep) room)) (mkS (mkCl it_NP adj))) ;
  EnemyDescription enemy power itemAttr =
    mkUtt (mkCl enemy (mkCN power (mkNP itemAttr)))
  
  
  -- Lexicon
  -- Moving directions
  Forward = mkNP (mkN "forward") ;
  Backward = mkNP (mkN "backward") ;
  Left = mkNP (mkN "left") ;
  Right = mkNP (mkN "right") ;

  RoomNumber i = mkNP (mkCN (mkN "room") (symb i)) ;
  
  -- Question directions
  Infront = mkPrep "in front of" ;
  Behind = mkPrep "behind" ;
  LeftSide = mkPrep "on the left of";
  RightSide = mkPrep "on the right of";
  
  -- Item locations as adverbs ("in my pockets", "in my backpack")
  Pockets = SyntaxEng.mkAdv in_Prep (mkNP (mkDet i_Pron) (mkN "pockets")) ;
  Backpack = SyntaxEng.mkAdv in_Prep (mkNP (mkDet i_Pron) (mkN "backpack")) ;
  Head = SyntaxEng.mkAdv on_Prep (mkNP (mkDet i_Pron) (mkN "head")) ;
  Feet = SyntaxEng.mkAdv on_Prep (mkNP (mkDet i_Pron) (mkN "feet")) ;
  Hands = SyntaxEng.mkAdv in_Prep (mkNP (mkDet i_Pron) (mkN "hands")) ;
  Pants = SyntaxEng.mkAdv in_Prep (mkNP (mkDet i_Pron) (mkN "pants")) ;
  
  Strong = mkN2 (mkN "strong") mkPrep "against" ;
  Weak = mkN2 (mkN "weak") mkPrep "against" ;

  -- Enemy nouns
  Orc = mkCN (mkN "orc") ;
  Goblin = mkCN (mkN "goblin") ;
  Dragon = mkCN (mkN "dragon") ;
  Minotaur = mkCN (mkN "minotaur") ;
  Mouse = mkCN (mkN "mouse") ;
  Tiger = mkCN (mkN "tiger") ;
  Bandit = mkCN (mkN "bandit") ;
  -- Enemy modifiers
  Angry = mkA "angry" ;
  Happy = mkA "happy" ;
  Depressed = mkA "depressed" ;
  EnemyMod adjective enemy = mkCN adjective enemy ;

  -- Item nouns
  Sword = mkCN (mkN "sword") ;
  Axe = mkCN (mkN "axe") ;
  Book = mkCN (mkN "book") ;
  Bread = mkCN (mkN "bread") ;
  Ring = mkCN (mkN "ring") ;
  Knife = mkCN (mkN "knife") ;
  Hammer = mkCN (mkN "hammer") ;
  Key = mkCN (mkN "key") ;

  -- Object nouns
  Boulder = mkCN (mkN "boulder") ;
  Door = mkCN (mkN "door") ;
  Exit = mkCN (mkN "exit") ;
  Gate = mkCN (mkN "gate") ;
  Chest = mkCN (mkN "treasure chest") ;
  Wall = mkCN (mkN "wall") ;
  Bag = mkCN (mkN "bag") ;

  -- Item modifiers
  Sharp = mkA "sharp" ;
  Dull = mkA "dull" ;
  Shiny = mkA "shiny" ;
  Fiery = mkA "fiery" ;
  Mysterious = mkA "mysterious" ;
  Frozen = mkA "frozen" ;
  ItemMod adjective item = mkCN adjective item ;

  -- Room descriptors
  Dark = mkA "dark" ;
  Damp = mkA "damp" ;
  Bright = mkA "bright" ;
  Creepy = mkA "creepy..." ; 
  Scary = mkA "scary" ;
  Peaceful = mkA "peaceful" ;

  -- Fight outcome verbs
  Win = mkV2 (mkV "win" "won" "won") ;
  Lose = mkV2 (mkV "lose" "lost" "lost") ;

  -- Useful verbs
  find_V2 = mkV2 (mkV "find" "found" "found") ;
  put_V2 = mkV2 (mkV "put" "put" "put");
  drop_V2 = mkV2 (mkV "drop") ;
  loot_V2 = mkV2 (mkV "loot") ;
  describe_V2 = mkV2 (mkV "describe") ;
  attack_V2 = mkV2 (mkV "attack") ;
  move_V2 = mkV2 (mkV "move") ;
  search_V2 = mkV2(mkV "search") ;


  ItemDescription adj = mkNP (mkCN adj (mkN "items"))

  Strong = mkA2 (mkA "strong") mkPrep "against" ; 
  Weak = mkA2 (mkA "weak") mkPrep "against" ;
}
