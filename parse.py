import gspread
from google.oauth2.service_account import Credentials
import re
import nltk
import spacy
import time
import tweepy
import os
nltk.download('punkt')

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('sheet-274815-b5805997d72c.json', scopes=scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TjRUke8rh-ohRE6b0IPcTffGHGl4HIQZXUUYYAehz0o/edit?usp=sharing')
worksheet_list = sh.worksheets()
print(worksheet_list)
sheet = worksheet_list[0]

# Define a dictionary based sentiment analysis

it_dict = {
    "abbandon":-2,"abbandonat":-2,"rapit":2,"abduzion":-2,"rapiment":2,"aborrir":-3,"aborrit":-3,"aberrant":-3,"aborrisc":-3,"abilità":2,"capacità":2,"bord":1,"assent":-1,"assolver":2,"assolt":2,"assolv":2,"assolvend":2,"assorbit":1,"abus":-3,"abusat":-3,"abusiv":-3,"accett":1,"accettat":1,"accettand":1,"incident":-2,"accidental":-2,"accidentalment":-2,"realizzar":2,"compiut":2,"comp":2,"accus":-1,"accusar":-2,"accusat":-2,"accusand":-2,"mal":-2,"realizzabil":1,"dolorant":-2,"acrimonious":-3,"attiv":1,"adeguat":1,"ammirar":3,"ammirat":3,"ammir":3,"ammirand":3,"ammetter":-1,
    "ammett":-1,"ammess":-1,"ammonir":-2,"ammonit":-2,"adottar":1,"adott":1,"adorabil":3,"ador":3,"adorat":3,"avanzat":1,"vantagg":2,"avventur":2,"avventuros":2,"colpit":-1,"affett":3,"affettuos":3,"afflitt":-2,"offes":-2,"paur":-2,"aggravar":-2,"aggravat":-2,"aggrav":-2,"aggravant":-2,"aggression":-2,"aggressiv":-2,"atterrit":-2,"agog":2,"agoniz":-3,"agonizzant":-3,"agonises":-3,"agonizz":-3,"d'accord":1,"gradevol":2,"concordat":1,"accord":1,"concord":1,"allarm":-2,"allarmat":-2,"allarmist":-2,"ahimè":-1,"avvisar":-1,"alienazion":-2,"viv":1,"allergic":-2,"consentir":1,"sol":2,
    "stupend":3,"stupir":3,"stupit":2,"stupisc":3,"sorprendent":3,"ambizios":2,"ambivalent":-1,"Amus":3,"divertit":3,"divertiment":4,"rabb":-2,"angers":-3,"arrabbiat":-3,"angosc":-2,"angosciat":-3,"animosità":-2,"infastidir":-2,"fastid":-2,"infastidit":-2,"fastidios":-2,"infastidisc":-2,"antagonist":-2,"contr":-1,"anticipazion":1,"ans":-2,"ansios":-2,"apatic":-2,"apat":-3,"apeshit":-3,"apocalittic":-2,"scusars":-1,"scusat":-1,"scus":-1,"scusandos":-1,"inorridit":-3,"spaventos":-2,"placar":2,"placat":3,"plac":2,"applaudir":2,"applaudit":2,"applaud":2,"applaus":2,"apprezzar":2,"apprezzat":2,
    "apprezz":2,"apprezzand":2,"apprezzament":2,"apprensiv":-2,"approvazion":2,"approvat":1,"approv":2,"ardent":1,"arrest":-1,"arrestat":-3,"arrogant":-2,"asham":-2,"vergogn":-2,"ass":-4,"assassin":-3,"risors":2,"attività":2,"assfucking":-4,"stronz":-4,"sbalordit":3,"incredibilment":3,"attacc":-1,"attaccat":-1,"attaccand":-1,"attacch":-1,"attrarr":1,"attratt":1,"attirand":2,"attrazion":2,"attra":1,"audac":2,"autorità":1,"scongiurar":-1,"scongiurat":-1,"scongiur":-1,"avid":-2,"evitar":-1,"evitat":-1,"evit":-1,"attender":-1,"attes":-1,"attend":-1,"prem":2,"assegnat":3,"impressionant":3,"terribil":-3,
    "imbarazzant":-2,"cartesian":-1,"backed":1,"support":2,"cazzut":-3,"salvatagg":2,"bamboozl":-2,"bamboozled":-2,"bamboozles":-2,"vietar":-2,"bandir":-1,"bancarott":-3,"bankster":-3,"vietat":-2,"affar":2,"barrier":-2,"bastard":-5,"battagl":-1,"battut":2,"beatific":3,"battit":-1,"bellezz":3,"bell":3,"ben":2,"abbellir":3,"sminuir":-2,"sminuit":-2,"amat":3,"benefic":2,"beneficiat":2,"beneficiand":2,"privera":-2,"lutt":-2,"bereaves":-2,"bereaving":-2,"miglior":2,"tradir":-3,"tradiment":-3,"tradit":-3,"tradisc":-3,"megl":2,"pregiudiz":-1,"di parte":-2,"grand":3,"cagn":-5,"femmin":-5,"amar":2,"amarament":-2,"bizzarr":-2,
    "bl":-2,"colp":-3,"incolp":-2,"benedic":2,"benedizion":3,"ciec":-1,"bliss":3,"beat":3,"blith":2,"blocc":-1,"successon":3,"bloccat":-2,"blocch":-1,"sanguinos":-3,"sfocat":-2,"vanaglorios":-2,"bold":2,"arditament":2,"bomb":-1,"aumentar":1,"potenziat":1,"aumentand":1,"amplific":1,"for":-2,"annoiat":-2,"noios":-2,"boicottagg":-2,"boicottat":-2,"coraggios":2,"svolt":3,"mozzafiat":5,"corromper":-3,"luminos":1,"brillant":4,"luminosità":1,"vivac":3,"rott":-1,"cov":-2,"bullism":-2,"stronzat":-4,"bull":-2,"bummer":-2,"oner":-2,"gravat":-2,"gravar":-2,"calm":2,"calmat":2,"calmant":2,"non può star":-3,"annullar":-1,"annullat":-1,
    "annulland":-1,"annull":-1,"cancr":-1,"grad":1,"affascinat":3,"cur":2,"spensierat":1,"attent":2,"incurant":-2,"freg":2,"incassar":-2,"ferit":-2,"catastrof":-3,"catastrofic":-4,"prudent":-1,"celebrar":3,"celebrat":3,"celebr":3,"celebrand":3,"censurar":-2,"censurat":-2,"censor":-2,"cert":1,"dispiacer":-2,"chagrined":-2,"sfidar":-1,"possibilità":2,"caos":-2,"caotic":-2,"caric":-3,"fascin":-3,"affascinant":3,"charmless":-3,"castigar":-3,"castigat":-3,"rimprover":-3,"castigand":-3,"imbrogliar":-3,"truffat":-3,"bar":-3,"imbroglion":-3,"trucch":-3,"allietar":2,"allietat":2,"allegr":3,"tif":2,"trist":-2,"custodir":2,"car":3,"tenerament":2,"coltivar":2,"chic":2,"infantil":-2,"agghiacciant":-1,"soffocar":-2,"soffocat":-1,"soffoc":-2,"soffocament":-2,"chiarisc":2,"chiarezz":2,"scontr":-1,"class":3,"pulit":2,"pulitor":2,"chiar":-1,"eliminat":1,"chiarament":1,"cancell":1,"intelligent":2,"offuscat":-1,"all'oscur":-2,"cazz":-4,"cocksucker":-5,"Cocksuckers":-5,"costrett":-1,"collass":-2,"crollat":-2,"croll":-2,"scontran":-1,"collision":-2,"collus":-3,"combattiment":-1,"combatt":-1,"commed":1,"comfort":2,"confortevol":2,"confortant":2,"confort":2,"elogiar":2,"lodat":3,"impegnars":1,"impegn":1,"commess":1,"commettend":1,"compassionevol":2,"competent":2,"competitiv":2,"compiacent":-2,"lamentan":-2,"lamentat":-2,"lament":-2,"complet":2,"conciliar":2,"conciliat":2,"concil":2,"conciliant":2,"condannar":-2,"condann":-2,"condannat":-2,"fiduc":1,"fiducios":2,"conflitt":-2,"conflittual":-2,"confonder":-2,"confus":-2,"confusion":-2,"Congrats":2,"congratulars":2,"congratulazion":2,"consens":2,"consolabl":2,"cospirazion":-3,"vincolat":-2,"contag":-2,"contagios":-1,"disprezz":-2,"sprezzant":-2,"sprezzantement":-2,"contender":-1,"contendent":-1,"sostenend":-1,"contenzios":-1,"contestabil":-2,"controvers":-2,"polemicament":-2,"convincer":1,"convint":-1,"convinc":1,"convivial":2,"fresc":1,"figo":3,"sfiga":-3,"cadaver":-1,"costos":-2,"coragg":2,"cortes":2,"vigliacc":-2,"vil":-3,"intimità":2,"cramp":-1,"merd":-3,"pazz":-3,"creativ":2,"mortificat":-2,"grid":-2,"crimin":-3,"criminal":-3,"cris":-3,"critic":-2,"criticar":-2,"criticat":-2,"criticand":-2,"crudel":-3,"crudeltà":-3,"schiacciar":-1,"schiacciat":-2,"schiacc":-1,"schiacciament":-1,"piang":-2,"piant":-2,"fic":-5,"curios":2,"maledir":-1,"tagliar":-2,"carin":2,"tagl":-1,"cinic":-2,"cinism":-2,"dann":-2,"dannatament":-4,"dannat":-3,"damnit":-4,"pericol":-2,"Daredevil":2,"scur":-2,"mort":-3,"assordant":-1,"debit":-2,"ingann":-2,"ingannevol":-3,"ingannar":-2,"ingannat":-2,"ingannand":-3,"decisiv":1,"dedicat":3,"sconfitt":-2,"difett":-3,"difensor":2,"indifes":-2,"rinviar":-1,"rimandand":-1,"sfid":-1,"deficit":-2,"degradar":-2,"degradat":-2,"degrad":-2,"disumanizzar":-2,"disumanizzat":-2,"disumanizz":-2,"disumanizzant":-2,"deprimer":-2,"sconsolat":-2,"dejecting":-2,"dejects":-2,"ritardar":-2,"ritardat":-2,"gio":3,"felic":3,"deliziand":3,"deliz":3,"domand":-1,"richiest":-1,"chiedend":-1,"dimostrazion":-1,"demoralizzat":-2,"negat":-2,"denar":-2,"negazionist":-2,"neg":-2,"denunciar":-2,"denunc":-2,"negar":-2,"negand":-2,"depress":-2,"depriment":-2,"deragliar":-2,"deragliat":-2,"deragl":-2,"derider":-2,"deris":-2,
    "derid":-2,"deridend":-2,"schern":-2,"desiderabil":2,"desider":1,"desiderat":2,"desideros":2,"disperazion":-2,"disperand":-3,"disper":-3,"disperat":-3,"disperatament":-3,"scoraggiat":-2,"distrugger":-3,"distrutt":-3,"distruggend":-3,"distrugg":-3,"distruzion":-3,"distruttiv":-3,"indipendent":-1,"detener":-2,"detenut":-2,"detenzion":-2,"determinat":2,"devastar":-2,"devastat":-2,"devastant":-2,"diamant":1,"minch":-4,"cazzon":-4,"difficil":-1,"diffident":-3,"dilemm":-1,"dipshit":-3,"dir":-3,"direful":-3,"sporc":-2,"disabilitazion":-1,"svantagg":-2,"svantaggiat":-2,"scompaion":-1,"scompars":-1,"scompar":-1,"deluder":-2,"delus":-2,"deludent":-2,"delusion":-2,"delud":-2,"disastr":-2,"disastros":-3,"creder":-2,"scartar":-1,"scartat":-1,"scartand":-1,"scart":-1,"disconsolation":-2,"scontent":-2,"discord":-2,"scontat":-1,"screditat":-2,"disonor":-2,"disonorat":-2,"mascherar":-1,"mascherat":-1,"travestiment":-1,"mascherand":-1,"disgust":-3,"disgustat":-3,"disgustos":-3,"disonest":-2,"disillus":-2,"disinclined":-2,"sconness":-2,"antipat":-2,"costernat":-2,"disturb":-2,"disorganizzat":-2,"disorientat":-2,"denigrar":-2,"denigrat":-2,"dispreg":-2,"denigrator":-2,"Contrariat":-2,"contestat":-2,"contestand":-2,"squalificat":-2,"inquietudin":-2,"disattes":-2,"trascurand":-2,"mancanz":-2,"rispett":-2,"mancat":-1,"interruzion":-2,"dirompent":-2,"insoddisfatt":-2,"distorcer":-2,"distort":-2,"distorcend":-2,"distorc":-2,"distrarr":-2,"distratt":-2,"distrazion":-2,"distra":-2,"affligg":-2,"angosciant":-2,"diffidenz":-3,"disturbar":-2,"disturbat":-2,"preoccupant":-3,"dithering":-2,"vertigin":-1,"schivar":-2,"dodgy":-2,"funzion":-3,"dolorous":-2,"piac":2,"dubb":-2,"dubitat":-1,"dubbios":-1,"dubitand":-1,"dubbi":-1,"dubitar":-2,"acquazzon":-3,"abbattut":-2,"downhearted":-2,"ribass":-2,"trascinar":-1,"trascinat":-1,"trascin":-1,"drenat":-2,"terror":-3,"temut":-2,"temend":-2,"sognar":1,"sogn":1,"droopy":-2,"cader":-1,"annegar":-2,"annegat":-2,"anneg":-2,"ubriac":-2,"dud":-2,"mut":-3,"idiot":-3,"discaric":-1,"scaricat":-2,"discarich":-1,"disfunzion":-2,"ser":2,"facilità":2,"facil":1,"estatic":4,"inquietant":-2,"efficac":2,"efficacement":2,"euforic":3,"esaltazion":3,"elegant":2,"elegantement":2,"imbarazz":-2,"imbarazzat":-2,"amareggiat":-2,"abbracciar":1,"emergenz":-2,"empatic":2,"vuot":-1,"incantat":2,"incoraggiar":2,"incoraggiat":2,"incoraggiament":2,"incoragg":2,"approvar":2,"omologat":2,"avall":2,"nemic":-2,"energic":2,"coinvolger":1,"assort":1,"goder":2,"godend":2,"dio":2,"illumin":2,"illuminat":2,"illuminant":2,"infuriar":-2,"infuriat":-2,"infuriant":-2,"rapir":3,"schiavizzar":-2,"asservit":-2,"schiavizz":-2,"garantir":2,"garantend":1,"intraprendent":1,"divertent":3,"affascinar":3,"entusiast":5,"affidat":2,"invid":-1,"invidios":-2,"erron":-2,"error":-2,"errar":-2,"sfuggir":-1,"sfugg":-1,"fug":-1,"stimat":2,"etic":2,"eufor":3,"sfratt":-1,"esagerar":-2,"esagerat":-2,"esager":-2,"esagerand":-2,"esasperat":2,"eccellenz":3,"eccellent":3,"eccitar":3,"eccitat":3,"eccitazion":3,"emozionant":3,"escluder":-1,"esclus":-2,"esclusion":-1,"Exclusiv":2,"scusar":-1,"esentar":-1,"esaurit":-2,"esilarant":2,"scagionar":2,"esonerat":2,"esoner":2,"esonerand":2,"ampliar":1,
    "espand":1,"espeller":-2,"espuls":-2,"espellend":-2,"espell":-2,"sfruttar":-2,"sfruttat":-2,"sfruttand":-2,"exploit":-2,"esplorazion":1,"esporr":-1,"espost":-1,"espon":-1,"esponend":-1,"estender":1,"estend":1,"esuberant":4,"exultant":3,"esultant":3,"favolos":4,"mod":-2,"FAG":-3,"faggot":-3,"fail":-2,"fallit":-2,"riesc":1,"falliment":-2,"debol":-2,"fier":2,"fed":1,"fedel":3,"fals":-5,"fingend":-1,"cadut":-2,"cad":-1,"falsificat":-3,"falsificar":-3,"fantastic":4,"fars":-1,"affascin":3,"fascist":-2,"decess":-3,"fatalità":-3,"affaticament":-2,"affaticat":-2,"fatich":-2,"faticos":-2,"favorir":2,"favorit":2,"preferit":2,"favorisc":2,"timoros":-2,"impavid":2,"temibil":-2,"Stuf":-3,"sensazion":1,"reat":-3,"fervent":2,"fervid":2,"festos":2,"fiasc":-3,"irrequiet":-2,"combatter":-1,"fuoc":-2,"sparat":-2,"cottur":-2,"montar":1,"fitness":1,"punt":2,"fugg":-1,"flop":-2,"influenz":-2,"agitat":-2,"focalizzat":2,"appassionat":2,"predilezion":2,"stupid":-2,"sciocch":-2,"preclusion":-2,"pignorament":-2,"dimenticar":-1,"smemorat":-2,"perdon":2,"indulgent":1,"dimenticat":-1,"fortunat":3,"frenetic":-1,"frod":-4,"truffator":-4,"fraudolenz":-4,"fraudolent":-4,"gratuit":1,"libertà":2,"frenes":-3,"accoglient":2,"spaventat":-2,"frikin":-2,"frisky":2,"accigliat":-1,"vanificar":-2,"frustrat":-2,"frustr":-2,"frustrant":-2,"frustrazion":-2,"ftw":3,"scopar":-4,"scopat":-4,"Fuckers":-4,"fuckfac":-4,"fuckhead":-4,"fucktard":-4,"fud":-3,"fuked":-4,"Fuking":-4,"adempier":2,"adempiut":2,"soddisf":2,"fumant":-2,"funeral":-1,"funky":2,"furios":-3,"inutil":-2,"gag":-2,"imbavagliat":-2,"guadagnar":2,"guadagnat":2,"guadagnand":2,"guadagn":2,"galant":3,"galantement":3,"galanter":3,"generos":2,"genial":3,"fantasm":-1,"vertiginos":-2,"regal":2,"glamour":3,"glamourous":3,"Gle":3,"oscurità":-1,"cup":-2,"glorios":2,"glor":2,"god":1,"pacch":4,"buon":3,"bontà":3,"graz":2,"grazios":3,"Grand":3,"grant":1,"concess":1,"concession":1,"sovvenzion":1,"grat":2,"gratificazion":2,"tomb":-2,"grig":-1,"maggior":3,"avidità":-3,"lavagg":-1,"salutar":1,"salutat":2,"salut":1,"dolor":-2,"addolorat":-2,"lord":-2,"crescent":1,"crescit":2,"garanz":1,"colpevol":-3,"credulità":-2,"credulon":-2,"pistol":-1,"h":2,"hacked":-1,"hah":3,"hahah":3,"hahahah":3,"grandin":2,"sfortunat":-2,"haplessness":-2,"felicità":3,"hardier":2,"disag":-2,"Hardy":2,"danneggiat":-2,"dannos":-2,"nuocer":-2,"Harms":-2,"tormentat":-2,"dur":-2,"odi":-3,"odiat":-3,"odiator":-3,"od":-3,"odiand":-3,"ritorcers":-1,"ossessionat":2,"Spettral":1,"ossession":-1,"san":2,"straziant":-3,"accorat":3,"ciel":2,"celest":4,"heavyhearted":-2,"infern":-4,"aiutar":2,"util":2,"aiutand":2,"impotent":-2,"aiut":2,"her":2,"heroes":2,"eroic":3,"esitant":-2,"esitat":-2,"nascos":-1,"nasconder":-1,"nascond":-1,"highlight":2,"ostacol":-2,"bufal":-2,"nostalg":-1,"onest":2,"onor":2,"onorat":2,"onorand":2,"hooligan":-2,"teppism":-2,"hooligans":-2,"sperar":2,"speranz":2,"sper":2,"sperand":2,"orrend":-3,"orribil":-3,"ostil":-2,"huckster":-2,"abbracc":2,"enorm":1,"humerous":3,"umiliat":-3,
    "umiliazion":-3,"humor":2,"umoristic":2,"fam":-2,"evviv":5,"ipocrit":-2,"ister":-3,"isteric":-3,"l'ignoranz":-2,"ignorant":-2,"ignorar":-1,"ignorat":-2,"ignor":-1,"ill":-2,"illegal":-3,"l'analfabetism":-2,"malatt":-2,"imbecill":-3,"immobilizzat":-1,"immortal":2,"immunitar":1,"impazient":-2,"imperfett":-2,"importanz":2,"important":2,"imporr":-1,"impost":-1,"impon":-1,"imponend":-1,"impressionar":3,"impressionat":-2,"impression":3,"imprigionat":-2,"migliorar":2,"migliorat":2,"migliorament":2,"migliorand":2,"incapacità":-2,"inazion":-2,"inadeguat":-2,"incapac":-2,"inabil":-2,
    "incensat":-2,"incompetenz":-2,"incompetent":-2,"sconsiderat":-2,"inconvenient":-2,"scomod":-2,"aumentat":1,"indecis":-1,"indistruttibil":2,"l'indifferenz":-2,"indifferent":-2,"indignat":-2,"indignazion":-2,"indottrinar":-2,"indottrinat":-2,"indottrin":-2,"inefficac":-2,"infatuat":2,"infatuazion":2,"infett":-2,"inferior":-2,"infiammat":-2,"influent":2,"violazion":-2,"esasperant":-3,"inibir":-1,"lesion":-2,"ingiustiz":-2,"innovar":1,"innov":1,"innovazion":1,"innovativ":2,"Inquisizion":-2,"foll":-3,"insicur":-2,"insensibil":-1,"insensibilità":-2,"insignificant":-2,"insipid":-2,"ispirazion":2,"ispirator":3,"ispirar":2,"ispirat":2,"ispir":2,"insult":-2,"insultat":-2,"offensiv":-2,"intatt":2,"integrità":2,"intens":1,"interess":1,"interessat":2,"interessant":2,"interrogat":-1,"interromper":-2,"interrott":-2,"interrompend":-2,"interromp":-2,"intimidir":-2,"intimidit":-2,"intimidisc":-2,"intimidator":-2,"intimidazion":-2,"intricat":2,"intrigh":1,"invincibil":2,"invitar":1,"invitand":1,"invulnerabil":2,"irat":-3,"ironic":-1,"iron":-1,"irrazional":-1,"irresistibil":2,"irresolut":-2,"irresponsabil":2,"irreversibil":-1,"irritar":-3,"irritat":-3,"irritant":-2,"isolat":-1,"prurit":-2,"jackass":-4,"somar":-4,"sbarazzin":2,"gelos":-2,"coglion":-3,"jesus":1,"gioiell":1,"gioiell":1,"unir":1,"scherz":2,"jolly":2,"giovial":2,"gioios":3,"joyless":-2,"giubilant":3,"giust":1,"giustiz":2,"giustament":2,"giustificat":2,"uccider":-3,"uccis":-3,"uccidend":-3,"uccid":-3,"tip":2,"Kinder":2,"bac":2,"Kudos":3,"mancan":-2,"lag":-2,"ritard":-2,"zopp":-2,"rider":1,"ris":1,"ridend":1,"rid":1,"laughting":1,"lanciat":1,"querel":-2,"caus":-2,"pigr":-1,"perdit":-3,"trapelat":-1,"lasciar":-1,"legal":1,"legalment":1,"letargic":-2,"letarg":-2,"bugiard":-3,"calunnios":-2,"mentit":-2,"salvavit":4,"com":2,"piaciut":2,"limitazion":-1,"limitat":-2,"limit":-2,"litigios":-2,"livid":-2,"detestat":-3,"detest":-3,"hall":-2,"lobbying":-2,"lol":3,"solitar":-2,"Lonesom":-2,"tela":-1,"incombev":-1,"incombent":-1,"sciolt":-3,"perd":-3,"perdent":-3,"perdend":-3,"pers":-2,"amabil":3,"amor":2,"lovelies":3,"bass":-1,"fedeltà":3,"fortun":3,"Fortunatament":3,"lugubrious":-2,"lunatic":-3,"nascondon":-1,"agguat":-1,"truccat":-1,"follement":-3,"obbligator":-1,"manipolat":-1,"manipoland":-1,"manipolazion":-1,"meravigl":3,"capolavor":4,"import":1,"cont":1,"matur":2,"significativ":1,"senz":-2,"medagl":3,"mediocrità":-3,"meditativ":1,"malincon":-2,"minacciar":-2,"minacciat":-2,"misericord":2,"Buon":3,"pasticc":-2,"incasinat":-2,"rovinar":-2,"metodic":2,"insensat":-2,"miracol":4,"ilarità":3,"miserabil":-3,"miser":-2,"misgiving":-2,"disinformazion":-2,"fuorviant":-3,"misread":-1,"inesatt":-2,"perder":-2,"mancant":-2,"sbagl":-2,"scambiand":-2,"fraintender":-2,"equivoc":-2,"fraintend":-2,"fraintes":-2,"gemev":-2,"gemit":-2,"fint":-1,"beffard":-2,"schernisc":-2,"mongering":-2,"monopolizzar":-2,"monopolizzat":-2,"monopolizz":-2,"Moody":-1,"mop":-1,"moping":-1,"Moron":-3,"motherfucker":-5,"fottut":-5,"motivar":1,"motivat":2,"motivant":2,"motivazion":1,"pianger":-2,"mumpish":-2,"omicid":-2,"mit":-1,"n00b":-2,"ingen":-2,"brutt":-3,"natural":1,"bisognos":-2,"negativ":-2,"negatività":-2,"trascuratezz":-2,"trascurat":-1,
    "trascur":-2,"nerv":-1,"nervos":-2,"nervosament":-2,"negr":-5,"nobil":2,"rumoros":-1,"nonsens":-2,"romanz":2,"nuoc":-3,"cancellar":-2,"cancellat":-2,"antipatic":-3,"oscen":-2,"obsolet":-2,"ostinat":-2,"dispar":-2,"offender":-2,"trasgressor":-2,"offend":-2,"offlin":-1,"OKS":2,"minaccios":3,"opportunità":2,"oppress":-2,"oppriment":-2,"ottimism":2,"ottimist":2,"optionless":-2,"clamor":-2,"scavalcat":-2,"oltragg":-3,"oltraggiat":-3,"outreach":2,"eccezional":5,"felicissim":4,"sovraccaric":-1,"reagir":1,"eccessiv":-1,"reagit":1,"semplificazion":-2,"semplificat":-2,"semplific":-2,"semplificar":-2,"esagerazion":-2,"sovrappes":-1,"ossimor":-1,"panic":-3,"paradis":3,"paradoss":-1,"perdonat":2,"perdonand":2,"parlamentar":-1,"passiv":-1,"passivament":-1,"patetic":-2,"pagar":-1,"pac":2,"pacific":2,"pacificament":2,"penalit":-2,"pensieros":-1,"perfett":3,"perfezionat":2,"perfettament":3,"perfezion":2,"autor":-2,"perpless":-2,"perseguitar":-2,"perseguitat":-2,"perseguit":-2,"perturbat":-2,"pessimism":-2,"pessimistic":-2,"pietrificat":-2,"fobic":-2,"pittoresc":2,"pileup":-1,"piq":-2,"piccat":-2,"piss":-4,"incazzat":-4,"pissing":-3,"piteous":-2,"compatit":-1,"peccat":-2,"giocos":2,"piacevol":3,"soddisfatt":2,"piacer":3,"bilic":-2,"velen":-2,"avvelenat":-2,"inquinar":-2,"inquinat":-2,"inquin":-2,"inquinator":-2,"pover":-2,"popolar":3,"positiv":2,"positivament":2,"possessiv":-2,"rinviat":-1,"rinv":-1,"rimandar":-1,"povertà":-1,"potent":2,"lod":3,"lodand":3,"pregar":1,"pregand":1,"preg":1,"prblm":-2,"prblms":-2,"preparat":1,"pression":-2,"fing":-1,"piuttost":1,"prevenir":-1,"impedit":-1,"impedend":-1,"impedisc":-1,"punger":-5,"carcer":-2,"prigionier":-2,"privilegiat":2,
    "proattiv":2,"problem":-2,"profittator":-2,"progress":2,"prominent":2,"promess":1,"promett":1,"promuover":1,"promoss":1,"promuov":1,"promuovend":1,"propagand":-2,"perseguir":-1,"perseg":-1,"prospettiv":1,"prosper":3,"protegger":1,"protett":1,"protegg":2,"protestar":-2,"manifestant":-2,"protestand":-2,"protest":-2,"orgogl":2,"provocar":-1,"provocat":-1,"provoc":-1,"provocand":-1,"pseudoscienz":-3,"punir":-2,"punit":-2,"punisc":-2,"punitiv":-2,"invadent":-1,"tremar":-2,"discutibil":-2,"interrogator":-1,"razzism":-3,"razzist":-3,"rabbios":-2,"piogg":-1,"rant":-3,"ranter":-3,"Ranters":-3,"sproloq":-3,"stupr":-4,"stuprator":-4,"visibil":2,"rapturous":4,"ratificat":2,"raggiunger":1,"raggiunt":1,"raggiung":1,"raggiungend":1,"rassicurar":1,"rassicurat":1,"rassicur":1,"rassicurant":2,"ribellion":-2,"recession":-2,"spericolat":-2,"raccomandar":2,"consigliat":2,"raccomand":2,"redent":2,"rifiutar":-1,"rifiutat":-2,"rifiutand":-1,"pentiret":-2,"rimpiant":-2,"pentit":-2,"rammaricandos":-2,"respint":-2,"resping":-1,"gioir":4,"gioit":4,"gioisc":4,"rallegrandos":4,"rilassat":2,"implacabil":-1,"affidament":2,"alleviar":1,"sollevat":2,"allev":1,"alleviand":2,"assaporand":2,"notevol":2,"rimors":-2,"respinger":-1,"salvat":2,"risentit":-2,"dimetters":-1,"dimess":-1,"dimissionar":-1,"dimett":-1,"risolut":2,"risolver":1,"risolt":1,"risolv":1,"risolvend":2,"rispettat":2,"responsabil":2,"reattiv":2,"riposant":2,"inquiet":-2,"ripristin":1,"restaurat":1,"limitar":-2,"limitand":-2,"restrizion":-2,"mantenut":-1,"ritirars":-1,"vendett":-2,"revengeful":-2,"riverit":2,"rilanciar":2,"ravviv":2,"ricompensat":2,"gratificant":2,"ricompens":2,"ricc":2,"ridicol":-3,"rig":-1,"rigoros":3,"rigorosament":3,"rivolt":-2,"risch":-2,"Rob":-2,"ladr":-2,"vestit":-2,"robing":-2,"derub":-2,"robust":2,"rofl":4,"Roflcopter":4,"roflma":4,"rovinat":-2,"rovinand":-2,"rovin":-2,"sabotar":-2,"rattristar":-2,"rattristat":-2,"purtropp":-2,"sicur":2,"salient":1,"sappy":-1,"sarcastic":-2,"salvar":2,"truff":-3,"scandal":-3,"scandalos":-3,"espiatorio":-2,"caprio":-2,"spaventar":-2,"scettic":-2,"sgridar":-2,"palett":3,"scornful":-2,"urlar":-2,"urlat":-2,"urland":-2,"url":-2,"avvitat":-3,"scumbag":-4,"fissat":2,"sedizion":-2,"sedizios":-2,"sedott":-1,"auto-illus":-2,"egoist":-3,"egoism":-3,"fras":-2,"seren":2,"grav":-2,"sexy":3,"traballant":-2,"vergognos":-2,"quot":1,"condivis":1,"azion":1,"frantum":-2,"shithead":-4,"scoss":-2,"scioccat":-2,"scioccant":-2,"urt":-2,"sparar":-1,"miop":-2,"carenz":-2,"toporagn":-4,"timid":-2,"malat":-2,"sigh":-2,"significatività":1,"silenziament":-1,"sincer":2,"sincerament":2,"sincerità":2,"peccaminos":-3,"scetticism":-2,"Slam":-2,"ridott":-2,"barr":-2,"tagliand":-2,"schiavitù":-3,"insonn":-2,"lisciant":2,"slickest":2,"lent":-2,"slut":-5,"strisc":-2,"smil":2,"sorris":2,"sorrident":2,"smog":-2,"subdol":-1,"snobbar":-2,"snobbat":-2,"snubbing":-2,"snobb":-2,"rifletter":1,"solenn":-1,"solid":2,"solidarietà":2,"soluzion":1,"solving":1,"lenir":3,"lenitiv":3,"sofisticat":2,"doloros":-3,"spam":-2,"spammer":-3,"spamming":-2,"scintill":1,"brillar":3,"sparkles":3,"frizzant":3,"speculativ":-2,"spirit":1,"spirited":2,"spiritless":-2,"dispettos":-2,"splendid":3,"arzill":2,"stab":-2,"pugnalat":-2,
    "stabil":2,"trafigg":-2,"stall":-2,"resistenz":2,"stamped":-2,"sorpres":-2,"affam":-2,"affamat":-2,"costant":2,"rubar":-2,"rub":-2,"stereotip":-2,"stereotipat":-2,"stimolar":1,"stimolat":1,"stimol":1,"stimoland":2,"avar":-2,"rubat":-2,"smetter":-1,"fermat":-1,"ferm":-1,"stout":2,"dritt":1,"stran":-2,"stranament":-1,"strangolat":-2,"forz":2,"rafforzar":2,"rafforzat":2,"rafforzand":2,"rafforz":2,"sottolineat":-2,"stress":-2,"scioper":-2,"attaccant":-2,"fort":2,"lottar":-2,"lottat":-2,"lott":-2,"lottand":-2,"testard":-2,"stordit":-2,"stordiment":4,"stupidament":-2,"suav":2,"sostanzial":1,"sostanzialment":1,"sovversiv":-2,"success":3,"succhiar":-3,"succh":-3,"soffrir":-2,"sofferenz":-2,"soffr":-2,"suicid":-2,"giudiz":-2,"bronc":-2,"imbronciat":-2,"super":3,"superb":5,"superior":2,"supportat":2,"sostenitor":1,"sopravvissut":2,"sopravvivend":2,"survivor":2,"sospett":-2,"sospettat":-1,"sospettand":-1,"sospender":-1,"sospes":-1,"giur":-2,"giurament":-2,"dolc":2,"rapid":2,"rapidament":2,"simpatic":2,"simpat":2,"tard":-2,"lacrim":-2,"gar":2,"tes":-2,"tension":-1,"terribilment":-3,"formidabil":4,"terrorizzat":-3,"terrorizzar":-3,"terrorizz":-3,"spinos":-2,"riflessiv":2,"minacc":-2,"minacciand":-2,"contrastar":-2,"contrastat":-2,"vanificazion":-2,"contrast":-2,"stanc":-2,"tett":-2,"tollerant":2,"sdentat":-2,"top":2,"strappat":-2,"tortur":-4,"torturat":-4,"torturand":-4,"totalitar":-2,"totalitarism":-2,"tout":-2,"propagandat":-2,"touting":-2,"bagarin":-2,"traged":-2,"tragic":-2,"tranquill":2,"trappol":-1,"intrappolat":-2,"traum":-3,"traumatic":-3,"travesty":-2,"treasonous":-3,"tesor":2,"tremor":-2,"tremul":-2,"trionfar":4,"trionfant":4,"gua":-2,"travagliat":-2,"ver":2,"fidat":2,"tumor":-2,"twat":-5,"inaccettabil":-2,"incompres":-2,"ignar":-2,"incredibil":-1,"incredul":-1,"imparzial":2,"incert":-1,"confermat":1,"accreditat":-1,"sottovalutar":-1,"sottovalutat":-1,"sottovalut":-1,"sottovalutand":-1,"minar":-2,"minat":-2,"min":-2,"minand":-2,"immeritevol":-2,"indesiderabil":-2,"disoccupazion":-2,"disugual":-1,"ineguagliabil":2,"immoral":-2,"ingiust":-2,"infelic":-2,"malsan":-2,"unificat":1,"unintelligent":-2,"unit":1,"immotivat":-2,"professional":2,"sconvolt":-2,"instabil":-2,"inarrestabil":2,"indesiderat":-2,"indegn":-2,"sconvolg":-2,"sconvolgent":-2,"urgent":-1,"utilità":2,"inutilità":-2,"vag":-2,"convalidar":1,"convalidat":1,"convalid":1,"verdett":-1,"acquisit":1,"vessazion":-2,"vibrant":3,"vizios":-2,"vittim":-3,"vittimizzar":-3,"vittimizz":-3,"vittimizzazion":-3,"vigil":3,"rivendicar":2,"rivendicat":2,"rivendic":2,"rivendicand":2,"violar":-2,"violat":-2,"viol":-2,"violand":-2,"violenz":-3,"violent":-3,"virtuos":2,"virulent":-2,"vision":1,"visionar":3,"visioning":1,"vitalità":3,"vitamin":1,"vetriol":-3,"vociferous":-1,"vulnerabilità":-2,"vulnerabil":-2,"segaiol":-3,"vuol":1,"guerr":-2,"cald":1,"calor":2,"avvertir":-2,"avvertit":-2,"warning":-3,"avvertenz":-3,"avvert":-2,"rifiut":-1,"sprecat":-2,"sprecar":-2,"vacillant":-1,"debolezz":-2,"ricchezz":3,"ricch":2,"pianget":-2,"benvenut":2,"accolt":2,"accogl":2,"capriccios":1,"calc":-3,"puttan":-4,"malvag":-2,"vedov":-1,"volontà":2,"vincer":4,"vincitor":4,"vincend":4,"vinc":4,"winwin":3,"desideran":1,"augur":1,"ritir":-3,"woebegon":-2,"meraviglios":4,"wo":3,"wooho":3,"woo":4,"woow":4,"indossat":-1,"preoccupat":-3,"preoccupars":-3,"pegg":-3,"peggiorar":-3,"peggiorat":-3,"peggiorament":-3,"peggior":-3,"degn":2,"wow":4,"wowow":4,"wowww":4,"adirat":-3,"relitt":-2,"sbagliat":-2,"tort":-2,"WTF":-4,"sì":1,"anelit":1,"yeees":2,"giovanil":2,"schif":-2,"gustos":3,"zelot":-2,"zelant":2
    }

def dict_based_sent(sent):
    words = nltk.word_tokenize(sent)
    score = 0.0
    for word in words:
        trunc = word[:-1]
        if trunc in it_dict.keys():
            score += it_dict[trunc]
    return score
        
dict_based_sent("Bimbi, anziani e famiglie messe in attesa, priorità alle sanatorie indiscriminate di clandestini.... NON è normale.")


# Parse Spreadsheet and tweet

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'])
auth.set_access_token(os.environ['TWITTER_TOKEN'], os.environ['TWITTER_TOKEN_SECRET'])

# Create API object
api = tweepy.API(auth)

nlp = spacy.load('it')

rows = sheet.row_count
print(rows)


f = open('salvinisays.tsv', 'r')
lines = f.readlines()

w = open('salvinisays.tsv', 'w')
w.write('sentence' + '\t' + 'link' + '\n')

for i in range(1, 100):
    time.sleep(2)
    row = sheet.row_values(str(i))
    sentence = row[2]
    
    sentence = sentence.replace('"','')
    sentence = sentence.replace('“','')
    sentence = sentence.replace('”','')
    
    doc = nlp(sentence)

    if dict_based_sent(sentence) < -1:
        
        for sentence in doc.sents:
            for token in sentence:
                
                if token.dep_ == 'nsubj' or token.dep_ == 'PROPN':
                    
                    # skip short words
                    children = [child for child in token.subtree]
                    
                    if len(children) < 2:
                        if(len(children[0]) < 4):
                            continue
                            
                    # skip links, hashtags and specific mentions
                    if 'http' in str(children) or '#' in str(children)  or ' io,' in str(children) or 'salvini' in str(children) or "dall'" in str(children) or "dell'" in str(children) :
                        continue
                    
                    tweet = ''

                    # append subj to tsv
                    for child in token.subtree: 
                        if ',' in str(child):
                            continue
                        tweet += str(child) + ' '
                    
                    # Check if already tweeted          
                    isTweeted = False
                    
                    for entry in lines:
                        if str(row[10]) in entry:
                            isTweeted = True
                            break
                        else:
                            isTweeted = False

                    if isTweeted == False:
                        # Without Mention
                        #api.update_status(tweet + ' https://twitter.com/matteosalvinimi/status/' + str(row[10]))
                        
                        # With Mention
                        #api.update_status(tweet + '#salvini #salviniflames @matteosalvinimi ' 'https://twitter.com/matteosalvinimi/status/' + str(row[10]))
                       
                        # Without Link
                        api.update_status(tweet)

                        w.write( str(tweet) + ' ' )
                        w.write('\t' + 'https://twitter.com/matteosalvinimi/status/' + str(row[10]) + ' \n') 
                        print('Tweeted:    ', tweet + '////  https://twitter.com/matteosalvinimi/status/' + str(row[10]) )
                        time.sleep(30)
                    
print('the end')
w.close()
f.close()
