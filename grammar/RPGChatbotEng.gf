concrete RPGChatbotEng of RPGChatbot = NumeralEng ** open
  Prelude,
  SymbolEng, --IntPN
  SyntaxEng,
  (S=SyntaxEng), -- mkAdv and lots of other small stuff
  NounEng,
  (NE=NounEng), -- usePN
  ParadigmsEng, --mkN, mkA, mkPrep, mkV2, mkV, mkA2
  ConstructorsEng,
  (C=ConstructorsEng) -- mkQuant
  in {

lincat
  Command = Imp ;
  Question = QCl ;
  Result = Utt ;
  Outcome = V2 ;
  Action = V2 ;
  Enemy = CN ;
  Item = CN ;
  Object = CN ;
  Location = CN ;
  Nouns = N ;
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
    mkImp (mkVP (mkVP attack_V2  (mkNP enemy)) (S.mkAdv with_Prep (mkNP item)))
    -- With articles, for grammatical correctness
    | mkImp (mkVP (mkVP attack_V2 (mkNP the_Det enemy)) (S.mkAdv with_Prep (mkNP the_Det item))) ;

  -- Looting enemies
  Loot enemy =
    mkImp loot_V2 (mkNP the_Det enemy)
    | mkImp search_V2 (mkNP the_Det enemy) ;

  -- Dropping items (getting rid of them)
  Drop item =
    mkImp drop_V2 (mkNP the_Det item) ;

  -- Moving items around locations (body parts, backpack, and pocketS.)
  Put item location =
      mkImp (mkVP (mkVP put_V2 (mkNP item)) (S.mkAdv to_Prep (mkNP location)))
    | mkImp (mkVP (mkVP put_V2 (mkNP the_Det item)) (S.mkAdv to_Prep (mkNP location))) ;

  -- Asking information about enemy.
  DescribeEnemy enemy =
    mkImp describe_V2 (mkNP the_Det enemy) ;

  -- [ QUESTIONS ]
  QDirectionQuery direction =
    mkQCl what_IP (S.mkAdv direction i_NP) ;

  QItemQuery location =
    -- Allowing "in" and "on" prepositions because it might change (in my backpack)
    mkQCl whatSg_IP ( S.mkAdv in_Prep ( mkNP ( C.mkQuant i_Pron ) location))
    | mkQCl whatSg_IP ( S.mkAdv on_Prep ( mkNP (  C.mkQuant i_Pron ) location )) ;


  --[CHATBOT ANSWERS]

  -- Finding items as a result of looting
  LootSuccess item =
    mkUtt (mkS pastTense (mkCl ( mkNP youSg_Pron ) find_V2 (mkNP a_Det item))) ;
  -- Result of Put action
  PutSuccess item location =
     mkUtt ( mkS pastTense ( mkCl you_NP ( mkVP ( mkVP put_V2 ( mkNP ( item ) ) ) ( S.mkAdv to_Prep ( mkNP ( C.mkQuant youSg_Pron ) location ) ) ) ) ) ;
  PutFail item =
    mkUtt (mkS negativePol (mkCl you_NP (mkVP (mkVP (mkVPSlash can8know_VV (mkVPSlash put_V2)) (mkNP item )) there7to_Adv))) ;
  -- Result of successful movement action
  MoveSuccess direction =
    mkUtt ( mkS pastTense ( mkCl ( mkNP youSg_Pron ) move_V2 direction ));
  -- Result of failed movement action (eg. There is a boulder blocking the way)
  MoveFail object =
    mkUtt ( mkS negativePol ( mkCl ( mkNP youSg_Pron ) ( mkVP ( mkVP ( mkVP can8know_VV ( mkVP (mkV "go") ) ) there7to_Adv ) ( S.mkAdv because_Subj ( mkS ( mkCl ( mkNP a_Quant object ) ) ) ) ) ) ) ;
  AttackSuccess enemy damage =
    mkUtt ( mkS and_Conj ( mkS ( mkCl ( mkNP youPol_Pron ) hit_V2 ( mkNP the_Quant enemy ) ) ) ( mkS pastTense ( mkCl ( mkNP it_Pron ) lose_V2 ( mkNP a_Quant ( mkNum ( mkCard damage ) ) health_N ) ) ) ) ;
  -- Telling that enemy doesn't exist.
  EnemyMissing enemy = mkUtt (mkS negativePol (mkCl (mkNP enemy) (mkV "exist"))) ;

  -- Telling that enemy has been encountered.
  EnemyEncountered enemy item = 
    mkUtt (mkCl (mkCN enemy (S.mkAdv with_Prep (mkNP a_Det item)))) ;
  EnemyAttack enemy damage =
    mkUtt ( mkS and_Conj ( mkS pastTense ( mkCl ( mkNP the_Quant enemy ) hit_V2 ( mkNP youPl_Pron ) ) ) ( mkS pastTense ( mkCl you_NP lose_V2 ( mkNP a_Quant ( mkNum ( mkCard damage ) ) health_N ) ) ) ) ;
  -- Telling what is in the direction.
  ADirectionQuery direction object =
    mkUtt ( mkS ( mkCl ( mkNP ( mkNP a_Quant object ) ( S.mkAdv direction ( mkNP youPl_Pron ) ) ) ) ) ;
  
  AItemQuery location =
    mkUtt ( mkS ( mkCl ( mkNP ( C.mkQuant youSg_Pron ) location ) have_V2 ( mkNP this_Quant pluralNum (mkN "item")))) ;

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
  RoomNumber i = mkNP (mkCN (mkN "room") (NE.UsePN (SymbolEng.IntPN i))) ;
  -- Question directions
  Infront = in8front_Prep ;
  Behind = behind_Prep ;
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
  Old = mkA "old" ;
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
  -- Basic nouns 
  health_N = mkN "health" "health" ;

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
  loot_V2 = mkV2 "loot" ;
  describe_V2 = mkV2 (mkV "describe") ;
  attack_V2 = mkV2 (mkV "attack") ;
  move_V2 = mkV2 (mkV "move") ;
  search_V2 = mkV2 (mkV "search") ;
  hit_V2 = mkV2 (mkV "hit" "hit" "hit") ;
  lose_V2 = mkV2 (mkV "lose" "lost" "lost") ;

  ItemType adj = mkNP (mkCN adj (mkN "items")) ;
  Strong = mkA2 (mkA "strong") (mkPrep "against") ; 
  Weak = mkA2 (mkA "weak") (mkPrep "against") ;

}
