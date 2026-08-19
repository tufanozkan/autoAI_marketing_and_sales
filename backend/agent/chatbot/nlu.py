import re
import unicodedata
from typing import Dict, Any, List, Optional, Tuple
from .state import CustomerContext, VehicleQueryCriteria

UNISEX_NAMES = {
    "deniz", "derya", "ege", "ozgur", "özgür", "utku", "yagmur", "yağmur", "gorkem", "görkem",
    "ilkay", "isik", "ışık", "bilge", "gunes", "güneş", "devrim", "umut", "evren", "sefa",
    "aytac", "aytaç", "tutku", "cagri", "çağrı", "gokay", "gökay", "eren", "ekin", "meric", "meriç",
    "toprak", "ruzgar", "rüzgar", "pamir", "goksel", "göksel", "sezer", "olcay", "safak", "şafak",
    "ufuk", "umit", "ümit", "hikmet", "fikret", "ismet", "servet", "yucel", "yücel", "ozlem", "özlem",
    "alaz", "ayhan", "ferhan", "hazar", "bulut", "seckin", "seçkin", "gokce", "gökçe", "cihan",
    "nimet", "sabah", "seval", "vecdi", "suat", "ugur", "uğur", "unal", "ünal", "vefa", "yasar", "yaşar"
}

FEMALE_NAMES = {
    "ceren", "ayse", "ayşe", "fatma", "elif", "zeynep", "merve", "busra", "büşra", "ebru", "esra",
    "ozge", "özge", "gamze", "selin", "damla", "irem", "eda", "asli", "aslı", "gizem", "tugba", "tuğba",
    "kubra", "kübra", "hazal", "hande", "sevgi", "nur", "emine", "hatice", "yasemin", "pinar", "pınar",
    "sinem", "duygu", "burcu", "didem", "defne", "eylul", "eylül", "azra", "ada", "lina", "arya",
    "mila", "masal", "beren", "melis", "melisa", "beste", "begum", "begüm", "sevil", "nil", "nilufer",
    "nilüfer", "gulsah", "gülşah", "songul", "songül", "filiz", "hülya", "hulya", "canan", "demet",
    "feride", "ilknur", "leyla", "melek", "neslihan", "nuray", "oyku", "öykü", "rabia", "seda",
    "sezen", "tuba", "tugce", "tuğçe", "ulku", "ülkü", "vildan", "zehra", "zumrut", "zümrüt",
    "alev", "aylin", "banu", "belgin", "berna", "betul", "betül", "beyza", "bige", "bihter",
    "birsen", "buket", "cansu", "ceyda", "cigdem", "çiğdem", "dilek", "ece", "ecem", "ela",
    "elvan", "emel", "fulya", "fusun", "füsun", "gonca", "gozde", "gözde", "gul", "gül",
    "gulay", "gülay", "gulden", "gülden", "guler", "güler", "gulfem", "gülfem", "gulsum", "gülsüm",
    "handan", "hale", "harika", "hilal", "ilgin", "ılgın", "isil", "ışıl", "iclal", "idil",
    "ipek", "jale", "kader", "kamile", "lale", "meltem", "mine", "muge", "müge", "naz",
    "nazan", "nazli", "nazlı", "necla", "nermin", "nesrin", "nevin", "nihal", "nihan", "nurten",
    "oya", "pelin", "peri", "reyhan", "ruya", "rüya", "saadet", "sanem", "sebnem", "şebnem",
    "senay", "şenay", "serife", "şerife", "sule", "şule", "simge", "suzan", "tulay", "tülay",
    "tulin", "tülin", "yasemen", "yesim", "yeşim", "yonca", "yeliz", "ahu", "ajda", "aksel",
    "arzu", "asuman", "aysel", "aysun", "ayten", "bahar", "basak", "başak", "belma", "benan",
    "bengi", "beril", "berrak", "billur", "burcak", "burçak", "candan", "cennet", "ceylan",
    "damlanur", "dicle", "dilara", "dilay", "diler", "ecrin", "edanur", "elcin", "elçin",
    "elifsu", "elmas", "esma", "fadime", "fatos", "fatoş", "fazilet", "feray", "feyza", "fidan",
    "figen", "fundanur", "funda", "gaye", "gulbahar", "gülbahar", "gulcan", "gülcan", "gulcin",
    "gülçin", "gulin", "gülin", "gullu", "güllü", "gulnihal", "gülnihal", "gulsima", "gülsima",
    "gunseli", "günseli", "guzide", "güzide", "habibe", "hacer", "hafize", "halide", "hanife",
    "hasibe", "havva", "hayrunnisa", "hicran", "hiranur", "hurrem", "hürrem", "husne", "hüsne",
    "ikbal", "ilkaynur", "imge", "inci", "ipeknur", "iremcan", "isra", "kardelen", "kayra",
    "kumru", "lalezar", "latife", "lemis", "maide", "makbule", "manolya", "maral", "mediha",
    "mehpare", "mehtap", "melike", "menekse", "menekşe", "meryem", "mihriban", "mimoza", "miray",
    "mualla", "muazzez", "muberra", "müberra", "mucella", "mücella", "munevver", "münevver",
    "mujde", "müjde", "mukaddes", "munise", "muruvvet", "mürüvvet", "naciye", "nadide", "nadire",
    "nafiye", "naime", "narin", "nazire", "nebahat", "nebihe", "nebile", "necmiye", "nefes",
    "nefise", "neriman", "nesibe", "neval", "nevra", "nezihe", "nida", "nigar", "nilay",
    "nisa", "nisanur", "nurcan", "nurgul", "nurgül", "nursel", "nursevim", "pakize", "parla",
    "perihan", "pervin", "rahime", "rana", "ravza", "raziye", "remziye", "rengin", "resmiye",
    "rukiye", "ruveyda", "rüveyda", "sabiha", "sabire", "sabriye", "safiye", "sahra", "saime",
    "sakine", "saliha", "salime", "samime", "saniye", "sarigul", "sarıgül", "secil", "seçil",
    "sedef", "seher", "sehriban", "şehriban", "selma", "selvi", "sema", "semanur", "semiha",
    "semiramis", "semra", "sena", "seniye", "serap", "seray", "seren", "serpil", "sevcan",
    "sevda", "sevde", "sevgul", "sevgül", "sevim", "sevinç", "sevtap", "sevval", "şevval",
    "seyhan", "seyma", "şeyma", "sibel", "sidika", "sıdıka", "sila", "sıla", "simay",
    "sirin", "şirin", "su", "sude", "sudenaz", "sukran", "şükran", "sukriye", "şükriye",
    "sumeyye", "sümeyye", "suna", "sureyya", "süreyya", "tanyeli", "tasvir", "tayyibe",
    "tenzile", "terken", "tevfika", "tomris", "tutkun", "tuvana", "turkan", "türkan",
    "ulviye", "umran", "ümran", "vahide", "vuslat", "yakut", "yaren", "yelda", "yildiz", "yıldız",
    "yosun", "zahide", "zarife", "zekiye", "zeliha", "zerrin", "zeyno", "ziba", "zinet",
    "ziynet", "zuhal", "zühal", "zuleyha", "züleyha", "zumra", "zümra"
}

MALE_NAMES = {
    "tufan", "ahmet", "mehmet", "mustafa", "ali", "burak", "emre", "onur", "oguz", "oğuz",
    "cem", "mert", "kaan", "kerem", "tolga", "serkan", "hakan", "erhan", "volkan", "gokhan",
    "gökhan", "murat", "serdar", "yusuf", "omer", "ömer", "halil", "ibrahim", "huseyin", "hüseyin",
    "ismail", "fatih", "selim", "sinan", "kemal", "koray", "alp", "alper", "efe", "doruk",
    "poyraz", "ayaz", "kuzey", "batu", "batuhan", "furkan", "enes", "berke", "ulas", "ulaş",
    "akin", "akın", "altan", "anil", "anıl", "atilla", "bahadir", "bahadır", "baki", "baran",
    "batur", "bayram", "berkay", "bilal", "bora", "bulent", "bülent", "caglar", "çağlar", "cahit",
    "caner", "cenk", "coskun", "coşkun", "cuneyt", "cüneyt", "davut", "demir", "dursun", "ekrem",
    "emin", "ender", "erdil", "erdogan", "erdoğan", "ergin", "erkan", "erol", "ersan", "ersin",
    "ertan", "ertugrul", "ertuğrul", "ferhat", "feridun", "giray", "guven", "güven", "hamdi",
    "hamza", "harun", "hayati", "haydar", "kadri", "kenan", "korkut", "kursat", "kürşat",
    "levent", "mansur", "mazhar", "metin", "mithat", "muhsin", "muzaffer", "naci", "nazmi",
    "necip", "nedim", "nihat", "niyazi", "nuh", "okan", "oktay", "orhan", "osman", "rasim",
    "recep", "remzi", "riza", "rıza", "sabri", "sadi", "saim", "salih", "samed", "samet",
    "sami", "sarp", "sedat", "semih", "sergen", "serhat", "sezgin", "suleyman", "süleyman",
    "sukru", "şükrü", "tahir", "tarik", "tarık", "taylan", "tekin", "tevfik", "timur",
    "turgay", "turhan", "vedat", "veysel", "yasin", "yavuz", "yunus", "zafer", "zekeriya",
    "zeki", "ziya", "abdullah", "abdurrahman", "adnan", "ahsen", "alişan", "alparslan", "altug",
    "altuğ", "aslan", "aybars", "aydin", "aydın", "azmi", "bahattin", "bahtiyar", "barbaros",
    "bedirhan", "bedri", "behzat", "bekir", "berdan", "berkin", "besim", "bilgehan", "birol",
    "boran", "bugra", "buğra", "candan", "celal", "celil", "cemil", "cengiz", "cetin", "çetin",
    "cevdet", "cihangir", "civanhir", "coskuner", "cumhur", "danyal", "dervis", "derviş",
    "dincer", "dinçer", "dogukan", "doğukan", "durmus", "durmuş", "edip", "ejder", "elvan",
    "ercument", "ercüment", "erdinc", "erdinç", "ergun", "ergün", "erim", "erkut", "erol",
    "ersin", "ertem", "esat", "evrensel", "eyup", "eyüp", "fahrettin", "fahri", "faruk",
    "faysal", "fazil", "fazıl", "fedai", "fehmi", "ferda", "ferit", "feyyaz", "feyzullah",
    "fikri", "fuat", "galip", "gani", "gencay", "gencaga", "gençağa", "gıyasettin", "gorkemli",
    "guclu", "güçlü", "gultekin", "gültekin", "guney", "güney", "gural", "güral", "gurbuz",
    "gürbüz", "gurkan", "gürkan", "gurol", "gürol", "habib", "habil", "hafiz", "hakkı",
    "haldun", "halilurrahman", "halis", "halit", "hamit", "hanefi", "hasip", "huseyin",
    "hüsrev", "idris", "ihsan", "ilhami", "ilhan", "ilter", "ilyas", "inam", "inal", "inan",
    "inanc", "inanç", "isak", "iskender", "islam", "ismailhakki", "izzet", "kadirhan", "kagan",
    "kağan", "kahraman", "kamer", "kamil", "kamuran", "kanat", "kandemir", "karahan", "kartal",
    "kasim", "kasım", "kayaalp", "kayahan", "kayhan", "kazim", "kazım", "kemalettin", "kenan",
    "keramet", "keremşah", "korcan", "koral", "korkmaz", "kutalmis", "kutay", "kutlu", "kutluk",
    "kutsal", "lami", "latif", "lokman", "lutfi", "lütfi", "macit", "mahfuz", "mahir", "malik",
    "mazlum", "mecnun", "medeni", "mehdi", "melik", "meliksah", "melikşah", "memduh", "menderes",
    "mengu", "mengü", "mercan", "merdan", "mertcan", "mervan", "mesut", "mete", "metehan",
    "mirac", "miraç", "mirza", "muammer", "mucahit", "mücahit", "mufit", "müfit", "muhammed",
    "muhittin", "muhtar", "mujde", "mukerrem", "mumin", "mümin", "mumtaz", "mümtaz", "munir",
    "münir", "murathan", "mursel", "mürsel", "murteza", "mürteza", "muslum", "müslüm", "mustafa",
    "mutlu", "mutluhan", "muzaffer", "nabi", "naci", "nadir", "nafiz", "nahit", "nail", "naim",
    "namik", "namık", "nasrettin", "nasuhi", "nazif", "nazim", "nazım", "nazmi", "nebahattin",
    "necati", "necdet", "necip", "necmattin", "nejat", "neset", "neşet", "nesim", "nevdil",
    "nevhiz", "nevzat", "neyzen", "nezih", "nihat", "nijat", "nilhan", "niyazi", "nizamettin",
    "noyan", "nuh", "nurettin", "nuri", "nurullah", "nusret", "oguzhan", "oğuzhan", "oguztürk",
    "oktay", "olgun", "omerfaruk", "omur", "ömür", "oral", "orhan", "orkun", "orkut", "ortac",
    "ortaç", "osman", "ozer", "özer", "ozgur", "özkan", "ozlem", "pasa", "paşa", "peker",
    "peyami", "piri", "polat", "polathan", "poyrazhan", "ragip", "ragıp", "rahmi", "raif",
    "ramazan", "rami", "rasim", "rasit", "raşit", "rauf", "recai", "recep", "refah", "refik",
    "reha", "remzi", "resat", "reşat", "resit", "reşit", "resul", "rifat", "rıfat", "riza",
    "rıza", "ruhi", "rusen", "ruşen", "rustu", "rüştü", "sabahattin", "sabri", "sadi", "sadik",
    "sadık", "sadri", "sadullah", "safa", "saffet", "sahap", "şahap", "sahin", "şahin", "saip",
    "sait", "salih", "salim", "samet", "sami", "samih", "saner", "sarper", "savas", "savaş",
    "saygin", "saygın", "seckin", "seçkin", "sedat", "sefa", "selahattin", "selami", "selcuk",
    "selçuk", "selim", "semih", "senol", "şenol", "serbülent", "sercan", "serdar", "sergen",
    "serhat", "serkan", "serkut", "server", "servet", "seyfi", "seyfullah", "seyit", "sezai",
    "sezer", "sezgin", "sinan", "siras", "sirri", "sırrı", "soner", "soykan", "soysal",
    "suat", "sukru", "şükrü", "suleyman", "süleyman", "tacettin", "tahir", "tahsin", "taj",
    "talat", "talha", "talip", "tamay", "tamer", "tan", "tanay", "taner", "tanju", "tankut",
    "tarik", "tarık", "tarkan", "taskin", "taşkın", "tayfun", "taylan", "tayyar", "tayyip",
    "tekin", "tekinalp", "temel", "tevfik", "tezcan", "timur", "timurhan", "tolga", "tolgahan",
    "tolunay", "tufan", "tugay", "tuğay", "tugberk", "tuğberk", "tunc", "tunç", "tuncay",
    "tuncel", "turan", "turgay", "turgut", "turhan", "turkay", "türkay", "turkcan", "türkcan",
    "turker", "türker", "tutkun", "ubeydullah", "ufuk", "ugur", "uğur", "ugurcan", "uğurcan",
    "ulass", "ulvi", "umit", "ümit", "umran", "umutcan", "unal", "ünal", "unsal", "ünsal",
    "uraz", "utku", "uygar", "uygur", "uzay", "uzer", "vafi", "vahap", "vahit", "vakur",
    "varol", "vasfi", "vedat", "vefa", "vehbi", "veli", "veysel", "veysi", "volkan", "vural",
    "yahya", "yakup", "yalcın", "yalçın", "yalin", "yalın", "yaman", "yasar", "yaşar",
    "yasin", "yavuz", "yavuzselim", "yekta", "yilmaz", "yılmaz", "yigit", "yiğit", "yigitcan",
    "yordam", "yucel", "yücel", "yuksel", "yüksel", "yurdaer", "yurdakul", "yusuf", "zafer",
    "zahit", "zekai", "zekeriya", "zeki", "zeynel", "ziya", "ziyad", "zulfu", "zülfü"
}

ALL_TURKISH_NAMES = UNISEX_NAMES | FEMALE_NAMES | MALE_NAMES

NON_NAME_WORDS = {
    "merhaba", "selam", "selamlar", "gunaydin", "günaydın", "iyi", "gunler", "günler", "aksamlar", "akşamlar",
    "telefon", "telefonu", "telefonum", "telefonumu", "telefonumuz", "telefonunuz", "numara", "numaram", "numaramı", "numarami", "numaramız", "numaranız",
    "vermek", "vermiyorum", "istemiyorum", "istemem", "paylasmak", "paylaşmak", "paylasamam", "paylaşamam", "yok", "gizli", "vermeyecigim", "vermeyecegim", "vermeyegim", "vermicem",
    "ben", "benim", "adim", "adım", "ismim", "adim soyadim", "adım soyadım", "adimi", "adımı",
    "araba", "arac", "araç", "aracın", "aracinin", "araciniz", "aracınızın", "aracim", "aracım", "arabalar", "araclar", "araçlar",
    "suv", "sedan", "hatchback", "crossover", "fiyat", "fiyati", "fiyatı", "km", "kilometre", "kilometresi",
    "vites", "sanziman", "şanzıman", "otomatik", "manuel", "yakit", "yakıt", "benzin", "dizel", "hibrit", "elektrik",
    "cam", "tavan", "sunroof", "isitma", "ısıtma", "koltuk", "direksiyon", "klima", "panoramik",
    "ekspertiz", "hasar", "kaza", "boya", "boyali", "boyalı", "degisen", "değişen", "tramer", "trameri", "garanti",
    "kredi", "finansman", "taksit", "takas", "pesinat", "peşinat", "faiz", "oran",
    "nerede", "adres", "showroom", "konum", "izmir", "gaziemir", "arkas", "spoticar",
    "peugeot", "citroen", "citroën", "honda", "fiat", "opel", "volvo", "skoda", "renault", "toyota", "volkswagen",
    "3008", "408", "2008", "5008", "508", "208", "c5", "city", "egea", "cross", "aircross", "mokka", "civic",
    "kac", "kaç", "ne", "neler", "var", "mi", "mı", "mu", "mü", "kadar", "üstü", "ustu", "alti", "altı", "uzeri", "üzeri",
    "cikart", "çıkart", "arttir", "arttır", "yukselt", "yükselt", "bilgi", "almak", "istiyorum", "bakiyorum", "bakıyorum", "ariyorum", "arıyorum",
    "randevu", "test", "surusu", "sürüşü", "oner", "öner", "baska", "başka", "model", "paket",
    "sadece", "hakkinda", "hakkında", "detay", "detaylar", "lutfen", "lütfen", "tesekkur", "teşekkür", "tesekkurler", "teşekkürler",
    "bey", "hanim", "hanım", "sayin", "sayın", "oyle", "öyle", "yapalim", "yapalım", "tamam", "tamamdır", "olur", "evet", "hayir", "hayır",
    "goster", "göster", "gosterir", "gösterir", "misin", "misiniz", "yeni", "sifir", "sıfır"
}

def norm(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("İ", "i")
        .replace("I", "i")
        .replace("ı", "i")
        .replace("ğ", "g")
        .replace("Ğ", "g")
        .replace("ü", "u")
        .replace("Ü", "u")
        .replace("ş", "s")
        .replace("Ş", "s")
        .replace("ö", "o")
        .replace("Ö", "o")
        .replace("ç", "c")
        .replace("Ç", "c")
        .lower()
        .strip()
    )

def is_valid_turkish_name(token: str) -> bool:
    n = norm(token)
    if not n or n in NON_NAME_WORDS:
        return False
    return n in ALL_TURKISH_NAMES

class NLUParser:
    @staticmethod
    def extract_phone(text: str) -> Tuple[Optional[str], bool, str]:
        clean = text
        phone = None
        m = re.search(r"(?:\+?90|0)?\s*(5\d{2})[\s.-]*(\d{3})[\s.-]*(\d{2})[\s.-]*(\d{2})", clean)
        if m:
            phone = f"0{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}"
            clean = clean[:m.start()] + " " + clean[m.end():]

        q_norm = norm(clean)
        
        # Robust decline detection regex & phrases
        decline_regex = r'\b(?:telefon(?:umu|um|umuzu|unuzu)?|numara(?:mı|mi|m|mızı|nızı)?)\s*(?:vermek|paylaşmak|paylasmak)?\s*(?:istemiyorum|istemem|vermeyeceğim|vermeyecigim|vermeyegim|vermicem|vermiyorum|paylaşamam|paylasamam|yok)\b|\b(?:vermeyeceğim|vermicem|vermiyorum)\b|\b(?:telefon|numara)\s*yok\b'
        
        phone_declined = bool(re.search(decline_regex, q_norm)) or any(p in q_norm for p in [
            "vermek istemiyorum", "paylasmak istemiyorum", "paylaşmak istemiyorum",
            "vermeyecegim", "vermicem", "vermiyorum", "numara yok", "telefon yok",
            "paylasamam", "paylaşamam", "telefonumu vermek", "numaramı vermek"
        ])

        return phone, phone_declined, clean

    @staticmethod
    def extract_name(text: str, has_existing_name: bool = False) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        if has_existing_name:
            return None, None, None

        clean_text = text.strip()
        
        # Mask phone decline statements so their tokens are never parsed as names
        masked_text = re.sub(
            r'\b(?:telefon(?:umu|um|umuzu|unuzu)?|numara(?:mı|mi|m)?)\s*(?:vermek|paylaşmak|paylasmak)?\s*(?:istemiyorum|istemem|vermeyeceğim|vermicem|vermiyorum|yok)\b',
            ' ',
            clean_text,
            flags=re.IGNORECASE
        )

        raw_first = None
        raw_last = None

        # Pattern 1: "adım [X] [Y]?" / "ismim [X] [Y]?" / "benim adım [X] [Y]?"
        p1 = re.search(r'(?:benim\s+adım|benim\s+ismim|adım\s+soyadım|adım|ismim)\s+([A-Za-zÇçĞğİıÖöŞşÜü]+)(?:\s+([A-Za-zÇçĞğİıÖöŞşÜü]+))?', masked_text, re.IGNORECASE)
        if p1:
            c1 = p1.group(1).strip()
            c2 = p1.group(2).strip() if p1.group(2) else None
            if is_valid_turkish_name(c1):
                raw_first = c1
                if c2 and norm(c2) not in NON_NAME_WORDS and re.match(r'^[A-Za-zÇçĞğİıÖöŞşÜü]{2,20}$', c2):
                    raw_last = c2

        # Pattern 2: "[X] [Y]? ben" / "[X] [Y]? benim"
        if not raw_first:
            p2 = re.search(r'\b([A-Za-zÇçĞğİıÖöŞşÜü]+)(?:\s+([A-Za-zÇçĞğİıÖöŞşÜü]+))?\s+(?:ben\b|benim\b|burada\b)', masked_text, re.IGNORECASE)
            if p2:
                c1 = p2.group(1).strip()
                c2 = p2.group(2).strip() if p2.group(2) else None
                if is_valid_turkish_name(c1):
                    raw_first = c1
                    if c2 and norm(c2) not in NON_NAME_WORDS and re.match(r'^[A-Za-zÇçĞğİıÖöŞşÜü]{2,20}$', c2):
                        raw_last = c2

        # Pattern 3: "ben [X]'im" / "ben [X] [Y]?"
        if not raw_first:
            p3_im = re.search(r'\bben\s+([A-Za-zÇçĞğİıÖöŞşÜü]+)(?:\x27?[iıuü]m)\b', masked_text, re.IGNORECASE)
            if p3_im:
                c1 = p3_im.group(1).strip()
                if is_valid_turkish_name(c1):
                    raw_first = c1
                    
        if not raw_first:
            p3 = re.search(r'\bben\s+([A-Za-zÇçĞğİıÖöŞşÜü]+)(?:\s+([A-Za-zÇçĞğİıÖöŞşÜü]+))?', masked_text, re.IGNORECASE)
            if p3:
                c1 = p3.group(1).strip()
                c2 = p3.group(2).strip() if p3.group(2) else None
                if is_valid_turkish_name(c1):
                    raw_first = c1
                    if c2 and norm(c2) not in NON_NAME_WORDS and re.match(r'^[A-Za-zÇçĞğİıÖöŞşÜü]{2,20}$', c2):
                        raw_last = c2

        # Pattern 4: Direct lexicon matching in tokens (e.g. "selam ceren")
        if not raw_first:
            tokens = [w.strip(" .,!?;:/-") for w in masked_text.split() if w.strip(" .,!?;:/-")]
            for idx, tok in enumerate(tokens):
                if is_valid_turkish_name(tok):
                    raw_first = tok
                    if idx + 1 < len(tokens):
                        next_tok = tokens[idx + 1]
                        if norm(next_tok) not in NON_NAME_WORDS and re.match(r'^[A-Za-zÇçĞğİıÖöŞşÜü]{2,20}$', next_tok):
                            raw_last = next_tok
                    break

        if raw_first:
            fn = raw_first.capitalize()
            ln = raw_last.capitalize() if raw_last else None
            full = f"{fn} {ln}".strip() if ln else fn
            return fn, ln, full

        return None, None, None

    @staticmethod
    def resolve_honorific(first_name: Optional[str], text: str, past_preference: Optional[str] = None) -> Tuple[Optional[str], bool]:
        # Critical Rule: If no first_name is present, honorific is ALWAYS None (NEVER BEY or HANIM)
        if not first_name:
            return None, False

        q_norm = norm(text)
        has_male_signal = bool(re.search(r'\b(?:bey|beyefendi|erkeğim|erkek)\b', q_norm))
        has_female_signal = bool(re.search(r'\b(?:hanım|hanim|hanımefendi|kadınım|kadinim|bayan)\b', q_norm))

        if has_male_signal and not has_female_signal:
            return "BEY", False
        if has_female_signal and not has_male_signal:
            return "HANIM", False

        if past_preference:
            return past_preference, False

        fn_norm = norm(first_name)
        if fn_norm in UNISEX_NAMES:
            return None, True
        elif fn_norm in FEMALE_NAMES:
            return "HANIM", False
        elif fn_norm in MALE_NAMES:
            return "BEY", False

        return None, False

    @staticmethod
    def _parse_single_price_str(raw: str) -> Optional[float]:
        if not raw: return None
        s = norm(raw).replace("tl", "").strip()
        
        # 1. Check composite '1 milyon 500 bin'
        m_comp = re.search(r'(\d+)\s*milyon\s*(\d+)\s*bin', s)
        if m_comp:
            return float(m_comp.group(1)) * 1_000_000.0 + float(m_comp.group(2)) * 1_000.0
            
        # 2. Check million '1.5m', '1,5 milyon', '2m'
        m_m = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:milyon|m\b)', s)
        if m_m:
            val = float(m_m.group(1).replace(",", "."))
            return val * 1_000_000.0 if val < 1000 else val
            
        # 3. Check thousand '800 bin', '800k'
        m_k = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:bin|k\b)', s)
        if m_k:
            val = float(m_k.group(1).replace(",", "."))
            return val * 1_000.0 if val < 1000 else val
            
        # 4. Standard digits e.g. '1.500.000', '2000000'
        m_dig = re.search(r'(\d{1,3}(?:\.\d{3}){1,3}|\d{5,9})', s)
        if m_dig:
            clean_num = m_dig.group(1).replace(".", "")
            return float(clean_num)
            
        # 5. Raw decimal '1.5' or '2'
        m_dec = re.search(r'(\d+(?:[.,]\d+)?)', s)
        if m_dec:
            val = float(m_dec.group(1).replace(",", "."))
            if val < 100:
                return val * 1_000_000.0
            elif val >= 50_000:
                return val
        return None

    @staticmethod
    def extract_budget(text: str) -> Tuple[Optional[float], Optional[float], bool]:
        q_norm = norm(text)
        
        # 1. Composite Range: '1 milyon 500 bin ile 2 milyon (arası)'
        comp_range = re.search(
            r'(\d+\s*milyon\s*\d+\s*bin)\s*(?:-|ile|ila|\s+ve\s+)\s*(\d+(?:[.,]\d+)?\s*(?:milyon|m\b)?|\d{1,3}(?:\.\d{3}){1,3})',
            q_norm
        )
        if comp_range:
            v1 = NLUParser._parse_single_price_str(comp_range.group(1))
            v2 = NLUParser._parse_single_price_str(comp_range.group(2))
            if v1 and v2:
                return min(v1, v2), max(v1, v2), True

        # 2. General Range: 'NUM1 (- / ile / ila / ve) NUM2 (arası)'
        range_m = re.search(
            r'(\d{1,3}(?:\.\d{3}){1,3}|\d+(?:[.,]\d+)?\s*(?:milyon|m\b|bin|k\b)?)\s*(?:-|–|—|ile|ila|\s+ve\s+)\s*(\d{1,3}(?:\.\d{3}){1,3}|\d+(?:[.,]\d+)?\s*(?:milyon|m\b|bin|k\b)?)(?:\s*arası|\s*arasi)?',
            q_norm
        )
        if range_m:
            part1 = range_m.group(1)
            part2 = range_m.group(2)
            v1 = NLUParser._parse_single_price_str(part1)
            v2 = NLUParser._parse_single_price_str(part2)
            if v1 and v2:
                if v1 < 1000 and v2 >= 1_000_000:
                    v1 = v1 * 1_000_000
                if v2 < 1000 and v1 >= 1_000_000:
                    v2 = v2 * 1_000_000
                if v1 >= 50_000 and v2 >= 50_000:
                    return min(v1, v2), max(v1, v2), True

        # 3. Single Composite: '1 milyon 500 bin'
        m_comp = re.search(r'(\d+)\s*milyon\s*(\d+)\s*bin', q_norm)
        if m_comp:
            val = float(m_comp.group(1)) * 1_000_000.0 + float(m_comp.group(2)) * 1_000.0
            return NLUParser._resolve_single_bound(val, q_norm)

        # 4. Single Million: '1.5 milyon', '1,5m', '2m'
        m_m = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:milyon|m(?=[^a-z]|$))', q_norm)
        if m_m:
            val = float(m_m.group(1).replace(",", ".")) * 1_000_000.0
            return NLUParser._resolve_single_bound(val, q_norm)

        # 5. Single Thousand: '800 bin', '800k'
        k_m = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:bin|k(?=[^a-z]|$))', q_norm)
        if k_m:
            val = float(k_m.group(1).replace(",", ".")) * 1_000.0
            return NLUParser._resolve_single_bound(val, q_norm)

        # 6. Digits: '1.500.000 TL', '1500000'
        dig_m = re.search(r'(\d{1,3}(?:\.\d{3}){1,3}|\d{5,9})\s*(?:tl)?', text, re.IGNORECASE)
        if dig_m:
            raw_str = dig_m.group(1).replace(".", "").replace(",", "")
            val = float(raw_str)
            if val >= 50_000:
                return NLUParser._resolve_single_bound(val, q_norm)

        return None, None, False

    @staticmethod
    def _resolve_single_bound(val: float, q_norm: str) -> Tuple[Optional[float], Optional[float], bool]:
        # Normalize punctuation for boundary check
        q_clean = q_norm.replace("'", " ").replace("’", " ")
        is_min = bool(re.search(r'\b(?:üstü|ustu|üzeri|uzeri|ve üzeri|ve uzeri|en az|en dusuk|en düşük|fazla|den fazla|dan fazla|yukarı|yukari|yukarısı|yukarisi)\b', q_clean))
        is_max = bool(re.search(r'\b(?:altı|alti|kadar|en fazla|en cok|en çok|gecmeyen|geçmeyen|asagisi|aşağısı|altinda|altında)\b', q_clean))

        if is_min and not is_max:
            return val, None, True
        elif is_max:
            return None, val, True
        else:
            return None, val, True

    @staticmethod
    def extract_vehicle_criteria(text: str) -> VehicleQueryCriteria:
        q_norm = norm(text)
        criteria = VehicleQueryCriteria()

        # Reset guard: Don't extract criteria if the user is asking for a reset
        reset_signals = [
            "yeni sohbet", "yeni konusma", "yeni konuşma", "sohbeti sifirla", "sohbeti sıfırla",
            "bastan basla", "baştan başla", "bastan baslayalim", "baştan başlayalım",
            "sohbeti temizle", "her seyi temizle", "her şeyi temizle",
            "filtreleri sifirla", "filtreleri sıfırla", "filtreleri temizle", "filtreleri kaldir", "filtreleri kaldır",
            "tum filtreleri temizle", "tüm filtreleri temizle", "tum filtreleri sifirla", "tüm filtreleri sıfırla",
            "bastan al", "baştan al"
        ]
        if any(w in q_norm for w in reset_signals) or q_norm in ["reset", "sifirla", "sıfırla", "temizle"]:
            return criteria

        # 1. Budget
        min_p, max_p, has_b = NLUParser.extract_budget(text)
        criteria.min_price = min_p
        criteria.max_price = max_p

        # 2. Brand
        brands = [
            ("citroen", "Citroën"), ("citroën", "Citroën"),
            ("peugeot", "Peugeot"), ("honda", "Honda"),
            ("fiat", "Fiat"), ("opel", "Opel"),
            ("volvo", "Volvo"), ("skoda", "Skoda"),
            ("renault", "Renault"), ("toyota", "Toyota"),
            ("volkswagen", "Volkswagen"), ("ford", "Ford")
        ]
        for b_key, b_val in brands:
            if re.search(r"\b" + re.escape(b_key) + r"\b", q_norm):
                criteria.brand = b_val
                break

        # 3. Model
        models = [
            ("408", "408", "Peugeot"),
            ("3008", "3008", "Peugeot"),
            ("2008", "2008", "Peugeot"),
            ("5008", "5008", "Peugeot"),
            ("c5 aircross", "C5 Aircross", "Citroën"),
            ("c5", "C5 Aircross", "Citroën"),
            ("aircross", "C5 Aircross", "Citroën"),
            ("city", "City", "Honda"),
            ("civic", "Civic", "Honda"),
            ("egea cross", "Egea Cross", "Fiat"),
            ("egea", "Egea Cross", "Fiat"),
            ("mokka", "Mokka", "Opel"),
            ("corsa", "Corsa", "Opel")
        ]
        for m_key, m_val, b_val in models:
            if re.search(r"\b" + re.escape(m_key) + r"\b", q_norm):
                criteria.model = m_val
                if not criteria.brand:
                    criteria.brand = b_val
                break

        # 4. Body type
        if "suv" in q_norm or "crossover" in q_norm or "cross" in q_norm:
            criteria.body_type = "SUV"
        elif "sedan" in q_norm:
            criteria.body_type = "Sedan"
        elif "hatchback" in q_norm or "hb" in q_norm:
            criteria.body_type = "Hatchback"

        # 5. Transmission & Negation
        if "manuel istemiyorum" in q_norm or "manuel olmasin" in q_norm or "duz vites istemiyorum" in q_norm or "düz vites istemiyorum" in q_norm:
            criteria.transmission = "automatic"
            criteria.transmission_excluded = "manual"
        elif "otomatik istemiyorum" in q_norm or "otomatik olmasin" in q_norm:
            criteria.transmission = "manual"
            criteria.transmission_excluded = "automatic"
        elif any(w in q_norm for w in ["otomatik", "eat8", "cvt", "dct", "otomatik vites"]):
            criteria.transmission = "automatic"
        elif any(w in q_norm for w in ["manuel", "duz vites", "düz vites"]):
            criteria.transmission = "manual"

        # 6. Fuel Type & Negation
        if "dizel olmasin" in q_norm or "dizel istemiyorum" in q_norm:
            criteria.fuel_type_excluded = "Dizel"
        elif "benzinli olmasin" in q_norm or "benzin istemiyorum" in q_norm:
            criteria.fuel_type_excluded = "Benzin"
        elif any(w in q_norm for w in ["dizel", "bluehdi", "multijet", "tdi"]):
            criteria.fuel_type = "Dizel"
        elif any(w in q_norm for w in ["benzin", "puretech", "i-vtec", "tsi"]):
            criteria.fuel_type = "Benzin"
        elif any(w in q_norm for w in ["hibrit", "hybrid"]):
            criteria.fuel_type = "Hibrit"
        elif any(w in q_norm for w in ["elektrik", "ev"]):
            criteria.fuel_type = "Elektrik"

        # 7. Features & Negation
        if "cam tavan istemiyorum" in q_norm or "cam tavan olmasin" in q_norm or "sunroofsuz" in q_norm:
            criteria.features_excluded.append("sunroof")
        elif any(w in q_norm for w in ["cam tavan", "sunroof", "panoramik"]):
            criteria.features.append("sunroof")

        if any(w in q_norm for w in ["koltuk isitma", "koltuk ısıtma", "isitma", "ısıtma", "direksiyon isitma"]):
            criteria.features.append("seat_heating")

        # 8. New Vehicle Request
        if any(w in q_norm for w in ["yeni bir arac", "yeni bir araç", "yeni araba", "yeni arac", "yeni araç", "sifir arac", "sıfır araç", "sifir araba", "sıfır araba", "sifir km", "sıfır km", "yeni araclardan", "yeni araçlardan", "2026 model", "sifir model", "sıfır model"]):
            criteria.is_new_vehicle_request = True

        return criteria

    @staticmethod
    def extract_question_aspects(text: str) -> List[str]:
        q_norm = norm(text)
        aspects = []

        is_asking_price = any(w in q_norm for w in ["fiyat", "fiyati", "fiyatı", "kac para", "kaç para", "ne kadar", "kaca", "kaça"]) and not any(w in q_norm for w in ["butce", "bütçe", "kadar", "cikart", "çıkart", "arttir", "arttır", "yukselt", "yükselt", "ustu", "üstü", "alti", "altı", "arasi", "arası"])
        if is_asking_price:
            aspects.append("price")

        if any(w in q_norm for w in ["km", "kilometre", "kilometresi", "kac binde", "kaç binde", "kac bin", "kaç bin", "mesafe", "kac km", "kaç km"]):
            aspects.append("mileage")

        if any(w in q_norm for w in ["vites", "vitesi", "sanziman", "şanzıman", "sanzimani", "şanzımanı", "otomatik mi", "manuel mi"]):
            aspects.append("transmission")

        if any(w in q_norm for w in ["yakit", "yakıt", "yakiti", "yakıtı", "tuketim", "tüketim", "benzin mi", "dizel mi", "ne yakar"]):
            aspects.append("fuel")

        if any(w in q_norm for w in ["motor", "beygir", "hp", "tork", "hizlanma", "hızlanma", "0-100", "cekis", "çekiş", "guc", "güç"]):
            aspects.append("engine")

        if any(w in q_norm for w in ["bagaj", "bagaji", "bagajı", "bagaj hacmi", "kac litre bagaj", "kaç litre bagaj"]):
            aspects.append("trunk")

        if any(w in q_norm for w in ["cam tavan", "sunroof", "panoramik"]):
            aspects.append("sunroof")

        if any(w in q_norm for w in ["koltuk isitma", "koltuk ısıtma", "direksiyon isitma", "isitma", "ısıtma", "masaj"]):
            aspects.append("heating")

        if any(w in q_norm for w in ["ekspertiz", "hasar", "kaza", "boya", "boyali", "boyalı", "degisen", "değişen", "tramer", "trameri", "durum", "durumu"]):
            aspects.append("expertise")

        if any(w in q_norm for w in ["donanim", "donanım", "donanimlar", "donanımları", "ozellik", "özellik", "ozellikler", "özellikleri", "paket"]):
            aspects.append("equipment")

        return aspects

    @staticmethod
    def extract_intents(text: str, has_customer_name: bool, has_phone: bool, phone_declined: bool, criteria: VehicleQueryCriteria, aspects: List[str]) -> List[str]:
        q_norm = norm(text)
        intents = []

        # 0. Conversation / Filter Reset Intent
        reset_signals = [
            "yeni sohbet", "yeni konusma", "yeni konuşma", "sohbeti sifirla", "sohbeti sıfırla",
            "bastan basla", "baştan başla", "bastan baslayalim", "baştan başlayalım",
            "sohbeti temizle", "her seyi temizle", "her şeyi temizle",
            "filtreleri sifirla", "filtreleri sıfırla", "filtreleri temizle", "filtreleri kaldir", "filtreleri kaldır",
            "tum filtreleri temizle", "tüm filtreleri temizle", "tum filtreleri sifirla", "tüm filtreleri sıfırla",
            "bastan al", "baştan al"
        ]
        if any(w in q_norm for w in reset_signals) or q_norm in ["reset", "sifirla", "sıfırla", "temizle"]:
            intents.append("CONVERSATION_RESET")
            return intents

        # 0.5. Inventory Query / Total Vehicle Count Intent
        inventory_query_signals = [
            "kac arac var", "kaç araç var", "kac araba var", "kaç araba var",
            "kac arac", "kaç araç", "kac araba", "kaç araba",
            "toplam arac", "toplam araç", "toplam kac", "toplam kaç",
            "stokta kac", "stokta kaç", "stok durumu",
            "tum araclar bunlar mi", "tüm araçlar bunlar mı", "butun araclar bunlar mi", "bütün araçlar bunlar mı",
            "3 arac goruyorum", "3 araç görüyorum", "arac sayisi", "araç sayısı",
            "tum stok", "tüm stok", "tum portfoy", "tüm portföy", "stokta ne var",
            "tum araclari goster", "tüm araçları göster", "tumunu goster", "tümünü göster",
            "butun araclari goster", "bütün araçları göster"
        ]
        if any(w in q_norm for w in inventory_query_signals) and not (criteria.brand or criteria.model or criteria.body_type or criteria.min_price or criteria.max_price):
            intents.append("INVENTORY_QUERY")

        if has_customer_name:
            intents.append("CUSTOMER_IDENTIFICATION")

        if has_phone:
            intents.append("PHONE_PROVIDED")

        if phone_declined:
            intents.append("PHONE_DECLINED")

        if any(w in q_norm for w in ["bey", "hanim", "hanım", "sayin", "sayın"]) and len(text.split()) <= 4 and not any(w in q_norm for w in ["suv", "sedan", "fiyat", "km", "arac"]):
            intents.append("HONORIFIC_PROVIDED")

        if criteria.is_new_vehicle_request:
            intents.append("NEW_VEHICLE_REQUEST")

        if any(w in q_norm for w in ["oyle yapalim", "öyle yapalım", "tamamdir", "tamamdır", "olur", "evet yapalim", "goster bakalim", "göster bakalım", "goster", "göster"]) and "CONVERSATION_RESET" not in intents and "INVENTORY_QUERY" not in intents:
            intents.append("CONFIRMATION")

        if any(w in q_norm for w in ["kadar cikart", "kadar çıkart", "kadar yukselt", "kadar yükselt", "butceyi", "bütçeyi", "butcemi", "bütçemi", "fiyat araligini", "arttir", "arttır", "cikar", "çıkar", "cikariyorum", "çıkarıyorum", "arasi", "arası"]):
            intents.append("BUDGET_UPDATE")

        if any(w in q_norm for w in ["takas", "eski arac", "aracimi vermek", "takasa", "degerleme", "değerleme"]):
            intents.append("TRADE_IN")

        if any(w in q_norm for w in ["kredi", "finansman", "taksit", "pesinat", "peşinat", "faiz", "vade", "banka"]):
            intents.append("FINANCE")

        if any(w in q_norm for w in ["nerede", "neredesiniz", "adres", "lokasyon", "konum", "gaziemir", "calisma saatleri", "çalışma saatleri"]):
            intents.append("LOCATION")

        if any(w in q_norm for w in ["garanti", "guvence", "güvence", "100 nokta", "kac nokta"]):
            intents.append("WARRANTY")

        if any(w in q_norm for w in ["randevu", "test surusu", "test sürüşü", "gelip gorebilir miyim", "gelip görebilir miyim"]):
            intents.append("APPOINTMENT")

        if aspects:
            intents.append("VEHICLE_DETAIL")

        if criteria.brand or criteria.model or criteria.body_type or criteria.min_price or criteria.max_price or criteria.features or criteria.transmission or criteria.fuel_type:
            intents.append("VEHICLE_SEARCH")

        if any(w in q_norm for w in ["oner", "öner", "onerir misin", "önerir misin", "baska ne var", "başka ne var", "farkli bir arac", "farklı bir araç", "en ucuz", "en uygun", "ekonomik", "en dusuk km", "en düşük km"]):
            intents.append("VEHICLE_RECOMMENDATION")

        if not intents and any(w in q_norm for w in ["merhaba", "selam", "gunaydin", "günaydın", "iyi gunler", "iyi günler", "hey"]):
            intents.append("GREETING")

        return intents
