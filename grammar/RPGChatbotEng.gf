concrete RPGChatbotEng of RPGChatbot = NumeralEng ** open
  Prelude,
  SymbolEng, --IntPN
  SyntaxEng,
  (S=SyntaxEng), -- mkAdv and lots of other small stuff
  NounEng, -- usePN
  (NE=NounEng),
  LexiconEng, -- now_Adv
  (L=LexiconEng), 
  ParadigmsEng, --mkN, mkA, mkPrep, mkV2, mkV, mkA2
  ConstructorsEng,
  (C=ConstructorsEng) -- mkQuant
  in {

lincat
  Command = Utt ;
  ProgramPrompt = QS ;
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
  QuestionDirection = Prep ;

lin
  -- [ COMMANDS ]
  -- Moving character
  Move dir =
    mkUtt (mkImp move_V2 dir);
  Attack enemy item =
    -- All article forms.
      mkUtt (mkImp (mkVP (mkVP attack_V2  (mkNP the_Det enemy)) (S.mkAdv with_Prep (mkNP item))))
    | mkUtt (mkImp (mkVP (mkVP attack_V2 (mkNP the_Det enemy)) (S.mkAdv with_Prep (mkNP the_Det item))))
    | mkUtt (mkImp (mkVP (mkVP attack_V2 (mkNP enemy)) (S.mkAdv with_Prep (mkNP the_Det item))))
    | mkUtt (mkImp (mkVP (mkVP attack_V2 (mkNP enemy)) (S.mkAdv with_Prep (mkNP item)))) ;
    
  AttackSameTarget item = 
    -- Attacking without target
    mkUtt (mkImp (mkVP (mkVP (mkV "attack")) (S.mkAdv with_Prep (mkNP the_Det item))))
    | mkUtt (mkImp (mkVP (mkVP (mkV "attack")) (S.mkAdv with_Prep (mkNP item)))) ;


  -- Looting enemies and entities
  Loot entity =
    mkUtt (mkImp loot_V2 (mkNP the_Det entity))
    | mkUtt (mkImp search_V2 (mkNP the_Det entity))
    | mkUtt (mkImp loot_V2 (mkNP entity))
    | mkUtt (mkImp search_V2 (mkNP entity)) ;

  -- Dropping items (getting rid of them)
  Drop item =
    mkUtt (mkImp drop_V2 (mkNP the_Det item))
    | mkUtt (mkImp drop_V2 (mkNP item)) ;

  -- Equiping items, similar to moving from location to location, but it is faster to type.
  -- Equip leather skirt
  Equip item =
    mkUtt (mkImp ( mkVP equip_V2 ( mkNP item ) ))
    | mkUtt (mkImp ( mkVP equip_V2 ( mkNP the_Det item ) )) ;
  -- For unequiping items, same as moving away from subinventory to backpack.
  Unequip item =
    mkUtt (mkImp ( mkVP unequip_V2 ( mkNP item ) ))
    | mkUtt (mkImp ( mkVP unequip_V2 ( mkNP the_Det item ) )) ;
  Open item object =
    -- All possibilities of phrase (with both determiners, 1/2, 0/2 determiners.)
      mkUtt (mkImp ( mkVP ( mkVP open_V2 ( mkNP the_Det object)) (S.mkAdv with_Prep (mkNP the_Det item))))
    | mkUtt (mkImp ( mkVP ( mkVP open_V2 ( mkNP the_Det object)) (S.mkAdv with_Prep (mkNP item))))
    | mkUtt (mkImp ( mkVP ( mkVP open_V2 ( mkNP object)) (S.mkAdv with_Prep (mkNP the_Det item))))
    | mkUtt (mkImp ( mkVP ( mkVP open_V2 ( mkNP object)) (S.mkAdv with_Prep (mkNP item)))) ;

  -- Asking information about enemy.
  DescribeEnemy enemy =
     mkUtt (mkImp describe_V2 (mkNP the_Det enemy)) 
    | mkUtt (mkImp describe_V2 (mkNP enemy)) ;

  -- [ QUESTIONS ]
  QDirectionQuery direction =
    mkUtt (mkQCl what_IP (S.mkAdv direction i_NP)) ;

  QItemQuery location =
    -- Allowing "in" and "on" prepositions because it might change (in my backpack)
    mkUtt (mkQCl whatSg_IP ( S.mkAdv in_Prep ( mkNP ( C.mkQuant i_Pron ) location)))
    | mkUtt (mkQCl whatSg_IP ( S.mkAdv on_Prep ( mkNP (  C.mkQuant i_Pron ) location ))) ;
  
  QEntityQuery temp =
    -- what is in this room
    mkUtt (mkQCl whatSg_IP (S.mkAdv in_Prep (mkNP this_Quant (NounEng.UseN room_N))))
    | mkUtt (mkQCl whatSg_IP (S.mkAdv (mkPrep "around") (mkNP i_Pron))) ;

  --[CHATBOT ANSWERS]

  -- Finding items as a result of looting
  -- "You found an old sword"
  LootSuccess item =
    mkUtt (mkS pastTense (mkCl ( mkNP youSg_Pron ) find_V2 (mkNP a_Det item))) ;

  -- You dropped sword
  DropSuccess item =
     mkUtt ( mkS pastTense ( mkCl ( mkNP youPol_Pron ) drop_V2 ( mkNP item ) ) ) ;
  
  -- Result of Move action
  -- "You put kilt to your legs."
  ItemMoveSuccess item location =
    mkUtt ( mkS pastTense ( mkCl you_NP ( mkVP ( mkVP put_V2 ( mkNP ( item ) ) ) ( S.mkAdv to_Prep ( mkNP ( C.mkQuant youSg_Pron ) location ) ) ) ) ) ;
  
  -- "You cannot put viking helmet there"
  ItemMoveFail item  =
    mkUtt (mkS negativePol (mkCl you_NP (mkVP (mkVP (mkVPSlash can8know_VV (mkVPSlash put_V2)) (mkNP item )) there7to_Adv))) ;
  
  -- "You can't equip that. "
  EquipFail item = 
    mkUtt ( mkS negativePol ( mkCl ( mkNP youPol_Pron ) ( mkVPSlash can8know_VV ( mkVPSlash equip_V2 ) ) ( mkNP a_Det item ) ) ) ;
  
  -- "<item name> was not equipped."
  UnequipFail item = 
    mkUtt ( mkS pastTense negativePol ( mkCl ( mkNP item ) ( passiveVP equip_V2 ) ) ) ;

  -- "You cannot do that because viking helmet is on head."
  ItemSlotTaken item location =
    mkUtt ( mkS negativePol ( mkCl ( mkNP youPol_Pron ) ( mkVP ( mkVP can_VV ( mkVP do_V2 ( mkNP ( mkDet that_Quant ) ) ) ) ( S.mkAdv because_Subj ( mkS ( mkCl ( mkNP item ) ( S.mkAdv on_Prep ( mkNP location ) ) ) ) ) ) ) ) ;

  -- Result of successful movement action
  MoveSuccess direction =
    mkUtt ( mkS pastTense ( mkCl ( mkNP youSg_Pron ) move_V2 direction ));

  -- Result of failed movement action (eg. There is a boulder blocking the way)
  MoveFail object =
    mkUtt ( mkS negativePol ( mkCl ( mkNP youSg_Pron ) ( mkVP ( mkVP ( mkVP can8know_VV ( mkVP (mkV "go") ) ) there7to_Adv ) ( S.mkAdv because_Subj ( mkS ( mkCl ( mkNP a_Quant object ) ) ) ) ) ) ) ;
  LootEnemyFail =
    mkUtt ( mkS negativePol ( mkCl ( mkNP youPol_Pron ) ( mkVP ( mkVP ( mkVPSlash can8know_VV ( mkVPSlash loot_V2 ) ) ( mkNP ( mkDet that_Quant ) ) ) ( S.mkAdv because_Subj ( mkS ( mkCl ( mkVP (mkA "alive") ) ) ) ) ) ) );
  AttackSuccess enemy damage =
    mkUtt ( mkS and_Conj ( mkS ( mkCl ( mkNP youPol_Pron ) hit_V2 ( mkNP the_Quant enemy ) ) ) ( mkS pastTense ( mkCl ( mkNP it_Pron ) lose_V2 ( mkNP a_Quant ( mkNum ( mkCard damage ) ) health_N ) ) ) ) ;
  -- There is nothing to attack.
  AttackFail =
    mkUtt ( mkS ( mkCl ( mkNP nothing_NP ( mkAdv to_Prep ( mkNP ( mkCN attack_N ) ) ) ) ) ) ;
  -- "You have 50 health left"
  PlayerHealth health =
    mkUtt ( mkS ( mkCl ( mkNP youPol_Pron ) have_V2 ( mkNP a_Quant ( mkNum ( mkCard health ) ) ( mkCN ( mkCN health_N ) ( mkNP ( mkDet a_Quant pluralNum left_Ord ) ) ) ) ) ) ;

  EnemyHealth enemy health = 
    mkUtt ( mkS ( mkCl ( mkNP the_Quant enemy ) have_V2 ( mkNP a_Quant ( mkNum ( mkCard health ) ) ( mkCN ( mkCN health_N ) ( mkNP ( mkDet a_Quant pluralNum left_Ord ) ) ) ) ) ) ;

  -- Telling that object doesn't exist.
  ObjectMissing object = mkUtt (mkS negativePol (mkCl (mkNP object) (mkV "exist"))) ;
  
  -- Telling that object is locked.
  ObjectLocked object =  mkUtt ( mkS ( mkCl ( mkNP object ) ( passiveVP lock_V2 ) ) ) ;
  
  -- Object has been unlocked.
  ObjectUnlocked object = 
    mkUtt ( mkS anteriorAnt ( mkCl ( mkNP object) (passiveVP unlock_V2))) ;

  -- Object cannot be opened.
  ObjectInvalidUnlock object =
    mkUtt ( mkS negativePol ( mkCl (mkNP object)  can8know_VV (passiveVP open_V2))) ;
  
    -- Object cannot be looted.
  ObjectInvalidLoot object =
    mkUtt ( mkS negativePol ( mkCl (mkNP object)  can8know_VV (passiveVP loot_V2))) ;

  -- "sword isn't a suitable item for that"
  InvalidUnlockItem item =
    mkUtt ( mkS negativePol ( mkCl ( mkNP item ) ( mkVP ( mkVP ( mkCN ( mkAP (mkA "suitable") ) ( mkCN (mkN "tool") ) ) ) ( S.mkAdv for_Prep ( mkNP ( mkDet that_Quant ) ) ) ) ) ) ;

  -- Telling user that an action cannot be done at the moment.
  InvalidAction =
     mkUtt ( mkS negativePol ( mkCl ( mkNP youPol_Pron ) ( mkVP ( mkVP ( mkVPSlash can8know_VV ( mkVPSlash do_V2 ) ) ( mkNP ( mkDet that_Quant right_Ord ) ) ) L.now_Adv ) ) ) ;
  -- Telling user that they cannot attack other targets while in a battle with one.
  BattleInvalidTarget enemy =
    mkUtt ( mkS negativePol ( mkCl ( mkNP youPol_Pron ) ( mkVP ( mkVP ( mkVPSlash can8know_VV ( mkVPSlash do_V2 ) ) ( mkNP ( mkDet that_Quant ) ) ) ( S.mkAdv because_Subj ( mkS ( mkCl ( mkNP youPol_Pron ) ( mkVP ( progressiveVP ( mkVP fight_V2 ( mkNP enemy ) ) ) already_Adv ) ) ) ) ) ) );

  ItemMissing item = 
    mkUtt ( mkS negativePol ( mkCl ( mkNP item ) ( mkVP ( mkVP can8know_VV ( passiveVP find_V2 ) ) ( S.mkAdv from_Prep ( mkNP ( C.mkQuant youPl_Pron ) inventory_N ) ) ) ) ) ;
  -- Telling that enemy has been encountered.
  EnemyEncountered enemy item = 
    mkUtt (mkCl (mkCN enemy (S.mkAdv with_Prep (mkNP a_Det item)))) ;
  -- Enemy hit you and you lost 20 health.
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

  -- The dragon is weak against sharp items and it has a hammer.
  EnemyDescWithItem enemy powerType itemKind item =
    mkUtt ( mkS and_Conj ( mkS ( mkCl ( mkNP the_Quant enemy ) ( mkVP ( mkVP powerType ) ( S.mkAdv (mkPrep "against") itemKind ) ) ) ) ( mkS ( mkCl ( mkVP have_V2 ( mkNP a_Quant item ) ) ) ) ) ;
  
  -- The dragon is weak against sharp items.
  EnemyDescWithoutItem enemy powerType itemKind = 
    mkUtt ( mkS ( mkCl ( mkNP the_Quant enemy ) ( mkVP ( mkVP powerType ) ( S.mkAdv (mkPrep "against") itemKind ) ) ) ) ;
  -- What will you do now?
  InputPrompt =
    mkQS futureTense ( mkQCl whatPl_IP ( mkClSlash ( mkClSlash youPol_NP ( mkVPSlash (mkV2 "do") ) ) L.now_Adv ) ) ;
  -- What is your next action?
  BattlePrompt =
    mkQS ( mkQCl ( mkIComp whatPl_IP ) ( mkNP ( C.mkQuant youPl_Pron ) ( mkCN ( mkAP (mkA "next") ) ( mkCN action_N ) ) ) ) ;

  -- Player death text.
  PlayerDeath =
    mkUtt ( mkS pastTense ( mkCl ( mkNP youPol_Pron ) die_V ) ) ;

  -- "You used <item>"
  ItemUse item =
     mkUtt ( mkS pastTense ( mkCl ( mkNP youPol_Pron ) use_V2 ( mkNP item ) ) ) ;

  -- You recovered <amount> health
  HealthRecover amount = 
     mkUtt ( mkS pastTense ( mkCl ( mkNP youPol_Pron ) recover_V2 ( mkNP a_Quant ( mkNum ( mkCard amount ) ) health_N ) ) ) ; 

  InvalidInput =
    mkUtt ( mkS negativePol ( mkCl ( mkNP i_Pron ) understand_V2 ( mkNP ( mkQuant youPl_Pron ) input_N ) ) );

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
  Troll = mkCN (mkN "troll") ;
  Goblin = mkCN (mkN "goblin") ;
  Dragon = mkCN (mkN "dragon") ;
  GiantRat = mkCN (mkN "giant rat") ;
  Ghoul = mkCN (mkN "ghoul") ;
  Demon = mkCN (mkN "demon") ;
  Skeleton = mkCN (mkN "skeleton") ;
  Wizard = mkCN (mkN "wizard") ;

  -- Enemy modifiers
  Infernal = mkA "infernal" ;
  Veteran = mkA "veteran" ;
  Young = mkA "young" ;
  Beefy= mkA "beefy" ;
  Rabid = mkA "rabid" ;
  -- Enemy traits
  Weak = mkA "weak" ;
  Strong = mkA "strong" ;
  
  EnemyMod adjective enemy = mkCN adjective enemy ;

  -- Item nouns
  Sword = mkCN (mkN "sword") ;
  Axe = mkCN (mkN "axe") ;
  Hammer = mkCN (mkN "hammer") ;
  WizardStaff = mkCN (mkN "wizard staff") ;
  Key = mkCN (mkN "key") ;
  PlatiniumSkirt = mkCN (mkN "platinium skirt") ;
  LeatherSkirt = mkCN (mkN "leather skirt") ;
  VikingHelmet = mkCN (mkN "viking helmet") ;
  BaseballCap = mkCN (mkN "baseball cap") ;
  UndyingTotem = mkCN (mkN "undying totem") ;

  -- Object nouns
  Boulder = mkCN (mkN "boulder") ;
  Door = mkCN (mkN "door") ;
  Exit = mkCN (mkN "exit") ;
  Gate = mkCN (mkN "gate") ;
  Chest = mkCN (mkN "treasure chest") ;
  Wall = mkCN (mkN "wall") ;
  Bag = mkCN (mkN "bag") ;
  PileOfBones = mkCN (mkN "pile of bones") ;
  EnemyObject enemy = mkCN enemy ;
  -- Basic nouns 
  health_N = mkN "health" "health" ;
  action_N = mkN "action" ;
  inventory_N = mkN "inventory" ;
  room_N = mkN "room" ;
  attack_N = mkN "attack" ;
  input_N = mkN "input" ;

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
  Creepy = mkA "creepy" ; 
  Scary = mkA "scary" ;
  Peaceful = mkA "peaceful" ;
  

  -- Fight outcome verbs
  Win = mkV2 (mkV "win" "won" "won") ;
  Lose = mkV2 (mkV "lose" "lost" "lost") ;

  -- Useful verbs
  drop_V2 = mkV2 (mkV "drop") ;
  loot_V2 = mkV2 "loot" ;
  describe_V2 = mkV2 (mkV "describe") ;
  attack_V2 = mkV2 (mkV "attack") ;
  recover_V2 = mkV2 (mkV "recover" ) ;
  use_V2 = mkV2 (mkV "use" ) ;
  move_V2 = mkV2 (mkV "move") ;
  search_V2 = mkV2 (mkV "search") ;
  lock_V2 = mkV2 (mkV "lock" "locked" "locked") ;
  unlock_V2 = mkV2 (mkV "unlock" "unlocked" "unlocked") ;
  equip_V2 = mkV2 (mkV "equip" "equipped" "equipped") ;
  unequip_V2 = mkV2 (mkV "unequip" "unequipped" "unequipped") ;

  -- "Sharp items"
  ItemType adj = mkNP (mkCN adj (mkN "items")) ;
}
