# Forma modelingizni loyihalash

Signal Forms modelga asoslangan yondashuvdan foydalanadi: formaning holati va tuzilmasi bevosita siz taqdim etgan modeldan hosil qilinadi. Model butun formaning asosi boʻlib xizmat qilgani uchun ishni yaxshi loyihalangan forma modelidan boshlash muhim. Bu qoʻllanma forma modellarini loyihalashning eng yaxshi amaliyotlarini koʻrib chiqadi.

## Forma modeli va domen modeli {#form-model-vs-domain-model}

Formalar foydalanuvchi kiritgan maʼlumotlarni yigʻish uchun ishlatiladi. Ilovangizda, ehtimol, bu maʼlumotlarni biznes logikasi yoki saqlash uchun qulay tarzda ifodalovchi domen modeli (domain model) mavjud. Biroq bu koʻpincha maʼlumotlarni formada qanday modellashtirmoqchi boʻlganimizdan _farq qiladi_.

Forma modeli foydalanuvchi kiritgan xom maʼlumotlarni UI'da koʻringan holida ifodalaydi. Masalan, formada foydalanuvchidan uchrashuv uchun sana va vaqt oraligʻini alohida input maydonlari sifatida tanlashni soʻrashingiz mumkin, hatto domen modelingiz buni yagona JavaScript `Date` obyekti sifatida ifodalasa ham.

```ts
interface AppointmentFormModel {
  name: string; // Appointment owner's name
  date: Date; // Appointment date (carries only date information, time component is unused)
  time: string; // Selected time as a string
}

interface AppointmentDomainModel {
  name: string; // Appointment owner's name
  time: Date; // Appointment time (carries both date and time information)
}
```

Formalar domen modelini shunchaki qayta ishlatish oʻrniga, maʼlumot kiritish tajribasiga moslashtirilgan forma modelidan foydalanishi kerak.

## Forma modelining eng yaxshi amaliyotlari {#form-model-best-practices}

### Aniq turlardan foydalaning {#use-specific-types}

[TypeScript turlaridan foydalanish](/guide/forms/signals/models#using-typescript-types) boʻlimida koʻrsatilganidek, modellaringiz uchun doimo interfeys yoki turlarni aniqlang. Aniq turlar yaxshiroq IntelliSense beradi, xatolarni kompilyatsiya vaqtida aniqlaydi va forma qanday maʼlumotlarni oʻz ichiga olishi haqida hujjat vazifasini oʻtaydi.

### Barcha maydonlarni initsializatsiya qiling {#initialize-all-fields}

Modelingizdagi har bir maydon uchun boshlangʻich qiymat bering:

```ts {prefer, header: 'All fields initialized'}
const taskModel = signal({
  title: '',
  description: '',
  priority: 'medium',
  completed: false,
});
```

```ts {avoid, header: 'Partial initialization'}
const taskModel = signal({
  title: '',
  // Missing description, priority, completed
});
```

Boshlangʻich qiymatlar yoʻq boʻlsa, oʻsha maydonlar maydonlar daraxtida (field tree) mavjud boʻlmaydi va forma bilan oʻzaro aloqada ularga murojaat qilish imkonsiz boʻladi.

### Modellarni aniq maqsadli saqlang {#keep-models-focused}

Har bir model bitta formani yoki oʻzaro bogʻliq maʼlumotlarning yaxlit toʻplamini ifodalashi kerak:

```ts {prefer, header: 'Focused on a single purpose'}
const loginModel = signal({
  email: '',
  password: '',
});
```

```ts {avoid, header: 'Mixing unrelated concerns'}
const appModel = signal({
  // Login data
  email: '',
  password: '',
  // User preferences
  theme: 'light',
  language: 'en',
  // Shopping cart
  cartItems: [],
});
```

Turli vazifalar uchun alohida modellar formalarni tushunish va qayta ishlatishni osonlashtiradi. Agar bir-biridan farqli maʼlumotlar toʻplamlarini boshqarayotgan boʻlsangiz, bir nechta forma yarating.

### Validatsiya talablarini hisobga oling {#consider-validation-requirements}

Modellarni validatsiyani koʻzda tutib loyihalang. Birga validatsiya qilinadigan maydonlarni guruhlang:

```ts {prefer, header: 'Related fields grouped for comparison'}
// Password fields grouped for comparison
interface PasswordChangeData {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}
```

Bunday tuzilma maydonlararo validatsiyani (masalan, `newPassword` `confirmPassword` bilan mos kelishini tekshirish) tabiiyroq qiladi.

### Maʼlumot turlarini UI boshqaruv elementlariga moslang {#match-data-types-to-ui-controls}

Forma modelingizdagi xususiyatlar UI boshqaruv elementlari (controls) kutadigan maʼlumot turlariga mos kelishi kerak.

Masalan, `size` maydoni (6, 12 yoki 24 donalik toʻplam) va `quantity` maydoniga ega ichimlik buyurtma formasini koʻrib chiqaylik. UI oʻlcham uchun ochiladigan roʻyxat (`<select>`), miqdor uchun esa sonli input (`<input type="number">`) ishlatadi.

Oʻlcham variantlari sonli koʻringani bilan, `<select>` elementlari satr qiymatlari bilan ishlaydi, shuning uchun `size` satr sifatida modellashtirilishi kerak. `<input type="number">` esa, aksincha, sonlar bilan ishlaydi, shu bois `quantity` son sifatida modellashtirilishi mumkin.

```ts {prefer, header: 'Appropriate data types for the bound UI controls'}
interface BeverageOrderFormModel {
  size: string; // Bound to: <select> (option values: "6", "12", "24")
  quantity: number; // Bound to: <input type="number">
}
```

### `undefined`'dan saqlaning {#avoid-undefined}

Forma modeli `undefined` qiymatlar yoki xususiyatlarni oʻz ichiga olmasligi kerak. Signal Forms'da forma tuzilmasi model tuzilmasidan hosil qilinadi va `undefined` boʻsh qiymatli maydonni emas, balki _maydonning yoʻqligini_ bildiradi. Bu shuni anglatadiki, ixtiyoriy maydonlardan (masalan, `{property?: string}`) ham saqlanishingiz kerak, chunki ular bilvosita `undefined`'ga yoʻl qoʻyadi.

Forma modelingizda boʻsh qiymatli xususiyatni ifodalash uchun UI boshqaruv elementi "boʻsh" deb tushunadigan qiymatdan foydalaning (masalan, `<input type="text">` uchun `""`). Agar maxsus UI boshqaruv elementini loyihalayotgan boʻlsangiz, "boʻsh"ni bildirish uchun koʻpincha `null` yaxshi qiymat boʻladi.

```ts {prefer, header: 'Appropriate empty values'}
interface UserFormModel {
  name: string; // Bound to <input type="text">
  birthday: Date | null; // Bound to <input type="date">
}

// Initialize our form with empty values.
form(signal({name: '', birthday: null}));
```

### Dinamik tuzilmali modellardan saqlaning {#avoid-models-with-dynamic-structure}

Agar forma modeli oʻz qiymatiga qarab shaklini oʻzgartirsa (obyektdagi xususiyatlar oʻzgarsa), u dinamik tuzilmaga ega boʻladi. Bu model turi turli shakldagi qiymatlarga yoʻl qoʻyganda yuz beradi, masalan, turli xususiyatlarga ega obyekt turlarining birlashmasi (union) yoki obyekt va primitiv turning birlashmasi. Quyidagi boʻlimlarda dinamik tuzilmali modellar jozibali koʻringani bilan, oxir-oqibat muammoli boʻlib chiqadigan bir nechta keng tarqalgan holatlar koʻrib chiqiladi.

#### Murakkab obyekt uchun boʻsh qiymat {#empty-value-for-a-complex-object}

Biz formalardan koʻpincha tizimdagi mavjud maʼlumotlarni tahrirlash uchun emas, balki foydalanuvchidan butunlay yangi maʼlumotlarni kiritishni soʻrash uchun foydalanamiz. Bunga yaxshi misol — hisob yaratish formasi. Uni quyidagi forma modeli yordamida modellashtirishimiz mumkin.

```ts
interface CreateAccountFormModel {
  name: {
    first: string;
    last: string;
  };
  username: string;
}
```

Formani yaratishda bir dilemmaga duch kelamiz: modeldagi boshlangʻich qiymat nima boʻlishi kerak? Foydalanuvchidan hali hech qanday maʼlumot olmaganimiz uchun `form<CreateAccountFormModel | null>()` yaratish jozibali tuyulishi mumkin.

```ts {avoid, header: 'Using null as empty value for complex object'}
createAccountForm = form<CreateAccountFormModel | null>(signal(/* what goes here, null? */));
```

Biroq Signal Forms _modelga asoslangan_ ekanini unutmaslik muhim. Agar modelimiz `null` boʻlsa va `null`da `name` yoki `username` xususiyati boʻlmasa, demak formamizda ham bu ichki maydonlar boʻlmaydi. Aslida bizga kerak boʻlgan narsa — barcha barg maydonlari boʻsh qiymatga oʻrnatilgan `CreateAccountFormModel` nusxasi.

```ts {prefer, header: 'Same shape value with empty values for properties'}
createAccountForm = form<CreateAccountFormModel>(
  signal({
    name: {
      first: '',
      last: '',
    },
    username: '',
  }),
);
```

Bu ifodadan foydalanganda bizga kerak boʻlgan barcha ichki maydonlar endi mavjud boʻladi va ularni shablonimizda `[formField]` direktivi yordamida bogʻlashimiz mumkin.

```html
First: <input [formField]="createAccountForm.name.first" /> Last:
<input [formField]="createAccountForm.name.last" /> Username:
<input [formField]="createAccountForm.username" />
```

#### Shartli yashirilgan yoki mavjud boʻlmagan maydonlar {#fields-that-are-conditionally-hidden-or-unavailable}

Formalar har doim ham chiziqli boʻlmaydi. Koʻpincha foydalanuvchining oldingi kiritgan maʼlumotlariga asoslanib shartli yoʻllar yaratish kerak boʻladi. Bunga misol — foydalanuvchiga turli toʻlov variantlarini taklif qiladigan forma. Bunday formaning UI'si qanday koʻrinishi mumkinligini tasavvur qilishdan boshlaylik.

```html
Name: <input type="text" />

<section>
  <h2>Payment Info</h2>
  <input type="radio" /> Credit Card @if (/* credit card selected */) {
  <section>
    Card Number <input type="text" /> Security Code <input type="text" /> Expiration
    <input type="text" />
  </section>
  }
  <input type="radio" /> Bank Account @if (/* bank account selected */) {
  <section>Account Number <input type="text" /> Routing Number <input type="text" /></section>
  }
</section>
```

Buni hal qilishning eng yaxshi yoʻli — _barcha_ mumkin boʻlgan toʻlov usullari uchun maydonlarni oʻz ichiga olgan statik tuzilmali forma modelidan foydalanish. Sxemamizda hozirda mavjud boʻlmagan maydonlarni yashirishimiz yoki oʻchirib qoʻyishimiz mumkin.

```ts {prefer, header: 'Static structure model'}
interface BillPayFormModel {
  name: string;
  method: {
    type: string;
    card: {
      cardNumber: string;
      securityCode: string;
      expiration: string;
    };
    bank: {
      accountNumber: string;
      routingNumber: string;
    };
  };
}

const billPaySchema = schema<BillPayFormModel>((billPay) => {
  // Hide credit card details when user has selected a method other than credit card.
  hidden(billPay.method.card, {when: ({valueOf}) => valueOf(billPay.method.type) !== 'card'});
  // Hide bank account details when user has selected a method other than bank account.
  hidden(billPay.method.bank, {when: ({valueOf}) => valueOf(billPay.method.type) !== 'bank'});
});
```

Bu modeldan foydalanganda `card` va `bank` obyektlarining ikkalasi ham forma holatida doimo mavjud boʻladi. Foydalanuvchi toʻlov usulini oʻzgartirganda biz faqat `type` xususiyatini yangilaymiz. Ular karta maydonlariga kiritgan maʼlumotlar `card` obyektida xavfsiz saqlanib qoladi va foydalanuvchi qaytib kelsa, qayta koʻrsatishga tayyor boʻladi.

Bundan farqli oʻlaroq, dinamik forma modeli dastlab bu holat uchun yaxshi mos kelayotgandek tuyulishi mumkin. Axir, foydalanuvchi "Credit Card"ni tanlagan boʻlsa, bizga hisob raqami va routing raqami maydonlari kerak emas. Buni diskriminatsiyalangan birlashma (discriminated union) sifatida modellashtirish istagi paydo boʻlishi mumkin:

```ts {avoid, header: 'Dynamic structure model'}
interface BillPayFormModel {
  name: string;
  method:
    | {
        type: 'card';
        cardNumber: string;
        securityCode: string;
        expiration: string;
      }
    | {
        type: 'bank';
        accountNumber: string;
        routingNumber: string;
      };
}
```

Biroq quyidagi vaziyatda nima boʻlishini oʻylab koʻring:

1. Foydalanuvchi ismini va kredit karta maʼlumotlarini toʻldiradi
2. Yuborishga chogʻlanadi, lekin soʻnggi lahzada xizmat haqiga koʻzi tushadi.
3. Haqdan qochish maqsadida bank hisobi variantiga oʻtadi.
4. Bank hisobi maʼlumotlarini kiritmoqchi boʻlganida ikkilanib qoladi: bu maʼlumotlarning qayerdadir sizib chiqishini istamaydi.
5. Yana kredit karta variantiga qaytadi, lekin hozirgina kiritgan barcha maʼlumotlar yoʻqolib qolganini koʻradi!

Bu dinamik tuzilmali forma modellarining yana bir muammosini koʻrsatadi: ular maʼlumot yoʻqolishiga sabab boʻlishi mumkin. Bunday model maydon yashirilgandan soʻng undagi maʼlumot boshqa hech qachon kerak boʻlmaydi deb hisoblaydi. U kredit karta maʼlumotlarini bank maʼlumotlari bilan almashtiradi va kredit karta maʼlumotlarini qaytarishning hech qanday yoʻli yoʻq.

#### Istisnolar {#exceptions}

Odatda statik tuzilma afzal koʻrilsa-da, dinamik tuzilma zarur boʻlgan va qoʻllab-quvvatlanadigan muayyan holatlar mavjud.

##### Massivlar {#arrays}

Massivlar eng keng tarqalgan istisnodir. Formalar koʻpincha oʻzgaruvchan miqdordagi elementlarni, masalan, telefon raqamlari, ishtirokchilar yoki buyurtmadagi mahsulotlar roʻyxatini yigʻishi kerak boʻladi.

```ts
interface SendEmailFormModel {
  subject: string;
  recipientEmails: string[];
}
```

Bu holda `recipientEmails` massivi foydalanuvchi forma bilan ishlashi davomida kengayadi va qisqaradi. Massiv uzunligi dinamik boʻlsa-da, alohida elementlarning tuzilmasi bir xil boʻlishi kerak (har bir element bir xil shaklga ega boʻlishi lozim).

##### UI boshqaruv elementi tomonidan atomar sifatida koʻriladigan maydonlar {#fields-that-are-treated-atomically-by-the-ui-control}

Dinamik tuzilma maqbul boʻlgan yana bir holat — murakkab obyekt UI boshqaruv elementi tomonidan yagona, atomar qiymat sifatida koʻrilganda. Yaʼni, boshqaruv elementi uning ichki maydonlariga alohida-alohida bogʻlanishga yoki murojaat qilishga urinmasa. Bunday vaziyatda boshqaruv elementi qiymatni ichki xususiyatlarini oʻzgartirish orqali emas, balki butun obyektni birdaniga almashtirish orqali yangilaydi. Bu holatda forma tuzilmasi ahamiyatsiz boʻlgani uchun uning dinamik boʻlishi maqbuldir.

Masalan, `location` maydonini oʻz ichiga olgan foydalanuvchi profili formasini koʻrib chiqaylik. Joylashuv koordinata obyektini qaytaruvchi murakkab "joylashuv tanlagich" vidjeti (ehtimol xarita yoki qidiruvli ochiladigan roʻyxat) yordamida tanlanadi. Joylashuv hali tanlanmagan yoki foydalanuvchi joylashuvini ulashishni istamagan holda tanlagich joylashuvni `null` sifatida bildiradi.

```ts {prefer, header: 'Dynamic structure is ok when field is treated as atomic'}
interface Location {
  lat: number;
  lng: number;
}

interface UserProfileFormModel {
  username: string;
  // This property has dynamic structure,
  // but that's ok because the location picker treats this field as atomic.
  location: Location | null;
}
```

Shablonda `location` maydonini bevosita maxsus boshqaruv elementimizga bogʻlaymiz:

```html
Username: <input [formField]="userForm.username" /> Location:
<location-picker [formField]="userForm.location"></location-picker>
```

Bu yerda `<location-picker>` butun `Location` obyektini (yoki `null`) qabul qiladi va qaytaradi, `userForm.location.lat` yoki `userForm.location.lng`'ga murojaat qilmaydi. Shuning uchun `location` modelga asoslangan formalar tamoyillarini buzmasdan bemalol dinamik shaklga ega boʻlishi mumkin.

## Forma modeli va domen modeli oʻrtasida oʻgirish {#translating-between-form-model-and-domain-model}

Forma modeli va domen modeli bir xil tushunchani turlicha ifodalagani uchun bu turli ifodalar oʻrtasida oʻgirish usuli bizga kerak boʻladi. Tizimdagi mavjud maʼlumotlarni foydalanuvchiga formada koʻrsatmoqchi boʻlganimizda, ularni domen modeli ifodasidan forma modeli ifodasiga aylantirishimiz kerak. Aksincha, foydalanuvchi oʻzgarishlarini saqlamoqchi boʻlganimizda, maʼlumotlarni forma modeli ifodasidan domen modeli ifodasiga aylantirishimiz kerak.

Tasavvur qilaylik, bizda domen modeli va forma modeli bor va ular oʻrtasida aylantirish uchun bir nechta funksiya yozganmiz.

```ts
interface MyDomainModel { ... }

interface MyFormModel { ... }

// Instance of `MyFormModel` populated with empty input (e.g. `''` for string inputs, etc.)
const EMPTY_MY_FORM_MODEL: MyFormModel = { ... };

function domainModelToFormModel(domainModel: MyDomainModel): MyFormModel { ... }

function formModelToDomainModel(formModel: MyFormModel): MyDomainModel { ... }
```

### Domen modelidan forma modeliga {#domain-model-to-form-model}

Tizimdagi mavjud domen modelini tahrirlash uchun forma yaratayotganimizda, odatda bu domen modelini forma komponentimizga `input()` sifatida yoki backend'dan (masalan, resource orqali) olamiz. Ikkala holatda ham `linkedSignal` oʻgirishimizni qoʻllash uchun ajoyib usul taqdim etadi.

Domen modelini `input()` sifatida olgan holda, input signalidan yoziladigan forma modelini yaratish uchun `linkedSignal`'dan foydalanishimiz mumkin.

```ts {prefer, header: 'Use linkedSignal to convert domain model to form model'}
@Component(...)
class MyForm {
  // The domain model to initialize the form with, if not given we start with an empty form.
  readonly domainModel = input<MyDomainModel>();

  private readonly formModel = linkedSignal({
    // Linked signal based on the domain model
    source: this.domainModel,
    // If domain model is defined convert it to a form model, otherwise use an empty form model.
    computation: (domainModel) => domainModel
      ? domainModelToFormModel(domainModel)
      : EMPTY_MY_FORM_MODEL
  });

  protected readonly myForm = form(this.formModel);
}
```

Shunga oʻxshab, domen modelini backend'dan resource orqali olganimizda, `formModel`'imizni yaratish uchun uning qiymatiga asoslangan `linkedSignal` yaratishimiz mumkin. Bu vaziyatda domen modelini olish biroz vaqt talab qilishi mumkin va maʼlumotlar yuklanguncha formani oʻchirib qoʻyishimiz kerak.

```ts {prefer, header: 'Disable or hide the form when data is unavailable'}
@Component(...)
class MyForm {
  // Fetch the domain model from the backend.
  readonly domainModelResource: ResourceRef<MyDomainModel | undefined> = httpResource(...);

  private readonly formModel = linkedSignal({
    // Linked signal based on the domain model resource
    source: this.domainModelResource.value,
    // Convert the domain model once it loads, use an empty form model while loading.
    computation: (domainModel) => domainModel
      ? domainModelToFormModel(domainModel)
      : EMPTY_MY_FORM_MODEL
  });

  protected readonly myForm = form(this.formModel, (root) => {
    // Disable the entire form when the resource is loading.
    disabled(root, {when: () => this.domainModelResource.isLoading()});
  });
}
```

Yuqoridagi misollar forma modelining bevosita domen modelidan sof hosil qilinishini koʻrsatadi. Biroq ayrim hollarda yangi domen modeli qiymati bilan oldingi domen modeli va forma modeli qiymatlari oʻrtasida yanada murakkab farqlash (diff) amalini bajarishni istashingiz mumkin. Buni `linkedSignal`'ning [oldingi holati](/guide/signals/linked-signal#accounting-for-previous-state) asosida amalga oshirish mumkin.

### Forma modelidan domen modeliga {#form-model-to-domain-model}

Foydalanuvchi kiritgan maʼlumotlarni tizimga qaytarib saqlashga tayyor boʻlganimizda, ularni domen modeli ifodasiga aylantirishimiz kerak. Bu odatda foydalanuvchi formani yuborganda yoki avtomatik saqlanadigan forma uchun foydalanuvchi tahrirlashi davomida uzluksiz yuz beradi.

Yuborishda saqlash uchun aylantirishni `submit` funksiyasida bajarishimiz mumkin.

```ts {prefer, header: 'Convert form model to domain model on submit'}
@Component(...)
class MyForm {
  private readonly myDataService = inject(MyDataService);

  protected readonly myForm = form<MyFormModel>(...);

  handleSubmit() {
    submit(this.myForm, async () => {
      await this.myDataService.update(formModelToDomainModel(this.myForm().value()));
    });
  };
}
```

Shuningdek, forma modelini bevosita serverga yuborib, forma modelidan domen modeliga
aylantirishni serverda bajarishingiz ham mumkin.

Uzluksiz saqlash uchun domen modelini `effect` ichida yangilang.

```ts {prefer, header: 'Convert form model to domain model in an effect for auto-saving'}
@Component(...)
class MyForm {
  readonly domainModel = model.required<MyDomainModel>()

  protected readonly myForm = form(...);

  constructor() {
    effect(() => {
      // When the form model changes to a valid value, update the domain model.
      if (this.myForm().valid()) {
        this.domainModel.set(formModelToDomainModel(this.myForm().value()));
      }
    });
  };
}
```

Yuqoridagi misollar forma modelidan domen modeliga sof aylantirishni koʻrsatadi. Biroq faqat forma modeli qiymatidan tashqari toʻliq forma holatini ham hisobga olish mutlaqo maqbuldir. Masalan, baytlarni tejash uchun serverga faqat foydalanuvchi oʻzgartirgan qismlar asosida qisman yangilanishlarni yuborishni istashimiz mumkin. Bu holda aylantirish funksiyamiz butun forma holatini qabul qilib, formaning qiymatlari va oʻzgartirilganlik (dirtiness) holatiga asoslangan siyrak domen modelini qaytaradigan tarzda loyihalanishi mumkin.

```ts
type Sparse<T> = T extends object ? {
    [P in keyof T]?: Sparse<T[P]>;
} : T;

function formStateToPartialDomainModel(
  formState: FieldState<MyFormModel>
): Sparse<MyDomainModel> { ... }
```
