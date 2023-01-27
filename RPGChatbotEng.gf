concrete RPGChatbotEng of RPGChatbot = open
  Prelude,
  SymbolEng,
  SyntaxEng,
  NounEng,
  ParadigmsEng,
  IdiomEng in {

lincat
  Command = Imp ;
  Question = Utt ;
  Result = Utt ;
  Outcome = V2 ;
  Action = V2 ;
  Enemy = CN ;
  Item = CN ;
  Object = CN ;
  Location = CN ;
  MoveDirection = NP ;
  Room = NP ;
  ItemDescription = NP ;
  EnemyAttribute = A ;
  ItemAttribute = A ;
  RoomAdjective = A ;
  EnemyPower = A2 ;
  QuestionDirection = Prep ;

lin
  -- [ COMMANDS ]
  -- Moving character
  Move dir =
    mkImp move_V2 dir;
  Attack enemy item =
    -- Without articles, just for quality of life
    mkImp (mkVP (mkVP attack_V2  (mkNP enemy)) (SyntaxEng.mkAdv with_Prep (mkNP item)))
    -- With articles, for grammatical correctness
    | mkImp (mkVP (mkVP attack_V2 (mkNP the_Det enemy)) (SyntaxEng.mkAdv with_Prep (mkNP the_Det item))) ;

  -- Looting enemies
  Loot enemy =
    mkImp loot_V2 (mkNP the_Det enemy)
    | mkImp search_V2 (mkNP the_Det enemy) ;

  -- Dropping items (getting rid of them)
  Drop item =
    mkImp drop_V2 (mkNP the_Det item) ;

  -- Moving items around locations (body parts, backpack, and pockets.)
  Put item location =
      mkImp (mkVP (mkVP put_V2 (mkNP item)) (SyntaxEng.mkAdv to_Prep (mkNP location)))
    | mkImp (mkVP (mkVP put_V2 (mkNP the_Det item)) (SyntaxEng.mkAdv to_Prep (mkNP location))) ;

  -- Asking information about enemy.
  DescribeEnemy enemy =
    mkImp describe_V2 (mkNP the_Det enemy) ;

  -- [ QUESTIONS ]
  QWhatIsInDirection direction =
    mkUtt (mkQCl what_IP (SyntaxEng.mkAdv direction i_NP)) ;

  QWhichItemsAre location =
    -- Allowing "in" and "on" prepositions because it might change (in my backpack, on my feet)
    mkUtt (mkQCl (mkIP whichPl_IDet (mkN "item")) (SyntaxEng.mkAdv in_Prep (mkNP (mkDet i_Pron) location)))
    | mkUtt (mkQCl (mkIP whichPl_IDet (mkN "item")) (SyntaxEng.mkAdv on_Prep (mkNP (mkDet i_Pron) location))) ;

  --[CHATBOT ANSWERS]

  -- Finding items as a result of looting
  LootSuccess item =
    mkUtt (mkS pastTense (mkCl you_NP find_V2 (mkNP a_Det item))) ;
  -- "You moved leather skirt to legs" - Result of Put action
  APut item location =
    mkUtt(mkS pastTense (mkCl you_NP (mkVP (mkVP (mkV2 "move")  (mkNP item)) (SyntaxEng.mkAdv to_Prep (mkNP location))))) ;

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
    mkUtt (mkCl (mkNP the_Det enemy) power itemAttr) ;
  
  
  -- Lexicon
  -- Moving directions
  Forward = mkNP (mkN "forward") ;
  Backward = mkNP (mkN "backward") ;
  Left = mkNP (mkN "left") ;
  Right = mkNP (mkN "right") ;

  RoomNumber i = mkNP (mkCN (mkN "room") (NounEng.UsePN (SymbolEng.IntPN i))) ;
  
  -- Question directions
  Infront = mkPrep "in front of" ;
  Behind = mkPrep "behind" ;
  LeftSide = mkPrep "on the left of";
  RightSide = mkPrep "on the right of";

  -- Item locations as nouns
  Backpack = mkCN (mkN "backpack") ;
  Head = mkCN (mkN "head") ;
  Legs = mkCN (mkN "legs") ;

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
  Hammer = mkCN (mkN "hammer") ;
  WizardStaff = mkCN (mkN "wizard staff") ;
  Key = mkCN (mkN "key") ;
  ScottishKilt = mkCN (mkN "Scottish kilt") ;
  LeatherSkirt = mkCN (mkN "leather skirt") ;
  VikingHelmet = mkCN (mkN "viking helmet") ;
  BaseballCap = mkCN (mkN "baseball cap") ;

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
  Magical = mkA "magical" ;
  Broken = mkA "broken" ;
  Legendary = mkA "legendary" ;
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
  search_V2 = mkV2 (mkV "search") ;

  ItemType adj = mkNP (mkCN adj (mkN "items")) ;
  Strong = mkA2 (mkA "strong") (mkPrep "against") ; 
  Weak = mkA2 (mkA "weak") (mkPrep "against") ;
}
