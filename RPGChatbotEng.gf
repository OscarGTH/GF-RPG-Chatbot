concrete RPGChatbotEng of RPGChatbot = open
  Prelude,
  SymbolicEng,
  SyntaxEng,
  ParadigmsEng,
  IdiomEng,
  QuestionEng in {

lincat
  Command = Imp ;
  Question = Utt ;
  Result = Utt ;
  Outcome = V2 ;
  Enemy = CN ;
  EnemyAttribute = A ;
  Item = CN ;
  ItemAttribute = A ;
  MoveDirection = NP ;
  QuestionDirection = Prep ;
  Location = Adv ;

lin
  -- [ COMMANDS ]
  -- Moving character
  Move dir =
    mkImp (mkV2 "move") dir;
  -- TODO: Add item that is attacked with or use the weapon in hands.
  Attack enemy item = 
    mkImp (mkV2 "attack") (mkNP the_Det enemy) ;
  -- Looting enemies
  Loot enemy =
    mkImp (mkV2 "loot") (mkNP the_Det enemy);
  Drop item =
    mkImp (mkV2 "drop") (mkNP the_Det item) ;
  -- TODO: Add location of where to put item to.
  Put item location =
    mkImp (mkV2 "put") (mkNP the_Det item) ;
  DescribeEnemy enemy =
    mkImp (mkV2 "describe") (mkNP the_Det enemy) ;


  -- [ QUESTIONS ]
  QWhatIsInDirection direction =
    mkUtt (mkQCl what_IP (SyntaxEng.mkAdv direction i_NP)) ;
  QWhichItemsAreIn location =
    mkUtt (mkQCl (mkIP whichPl_IDet (mkN "item")) location) ;
  --[Chatbot answers]
  -- Finding items as a result of looting
  LootSuccess item =
    mkUtt (mkCl you_NP (mkV2 "find") (mkNP item)) ;
  -- Telling that enemy doesn't exist.
  EnemyMissing enemy = mkUtt (mkS negativePol (mkCl (mkNP enemy) (mkV "exist"))) ;
  -- Telling that enemy has been encountered.
  EnemyEncountered enemy item = 
    mkUtt (mkCl (mkCN enemy (SyntaxEng.mkAdv with_Prep (mkNP a_Det item)))) ;
  -- Outcome of the fight (Whether enemy won or lost.)
  FightResult enemy outcome =
    mkUtt (mkS pastTense (mkCl (mkNP the_Det enemy) outcome (mkNP the_Det (mkN "fight")))) ;
  
  -- Lexicon
  -- Moving directions
  Forward = mkNP (mkN "forward") ;
  Backward = mkNP (mkN "backward") ;
  Left = mkNP (mkN "left") ;
  Right = mkNP (mkN "right") ;

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



  -- Enemy nouns
  Orc = mkCN (mkN "orc") ;
  Goblin = mkCN (mkN "goblin") ;
  Dragon = mkCN (mkN "dragon") ;
  Snake = mkCN (mkN "snake") ;
  Mouse = mkCN (mkN "mouse") ;
  Tiger = mkCN (mkN "tiger") ;
  Shark = mkCN (mkN "shark") ;
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
  -- Item modifiers
  Sharp = mkA "sharp" ;
  Dull = mkA "dull" ;
  Shiny = mkA "shiny" ;
  Fiery = mkA "fiery" ;
  Mysterious = mkA "mysterious" ;
  Frozen = mkA "frozen" ;
  ItemMod adjective item = mkCN adjective item ;

  -- Fight outcome verbs
  Win = mkV2 (mkV "win" "won" "won") ;
  Lose = mkV2 (mkV "lose" "lost" "lost") ;

}
