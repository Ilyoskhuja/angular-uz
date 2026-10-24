# Forma modellari

Forma modellari Signal Forms'ning asosi boʻlib, forma maʼlumotlaringiz uchun yagona haqiqat manbai (single source of truth) vazifasini bajaradi. Ushbu qoʻllanma forma modellarini qanday yaratish, yangilash va ularni qoʻllab-quvvatlash qulay boʻladigan tarzda loyihalashni koʻrib chiqadi.

NOTE: Forma modellari Angular'ning komponentlarda ikki tomonlama bogʻlash uchun ishlatiladigan `model()` signalidan farq qiladi. Forma modeli — forma maʼlumotlarini saqlaydigan yoziladigan (writable) signal, `model()` esa ota/bola komponentlar oʻrtasidagi aloqa uchun input/output'lar yaratadi.

## Forma modellari qanday muammoni hal qiladi {#what-form-models-solve}

Formalar vaqt oʻtishi bilan oʻzgaradigan maʼlumotlarni boshqarishni talab qiladi. Aniq tuzilma boʻlmasa, bu maʼlumotlar komponent xususiyatlari boʻylab tarqalib ketishi mumkin, bu esa oʻzgarishlarni kuzatish, kiritilgan maʼlumotlarni tekshirish yoki ularni serverga yuborishni qiyinlashtiradi.

Forma modellari buni forma maʼlumotlarini yagona yoziladigan signalda markazlashtirish orqali hal qiladi. Model yangilanganda forma bu oʻzgarishlarni avtomatik aks ettiradi. Foydalanuvchilar forma bilan ishlaganda model shunga mos ravishda yangilanadi.

## Modellar yaratish {#creating-models}

Forma modeli — Angular'ning `signal()` funksiyasi bilan yaratilgan yoziladigan signal. Signal formangizning maʼlumotlar tuzilmasini ifodalovchi obyektni saqlaydi.

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField} from '@angular/forms/signals';

@Component({
  selector: 'app-login',
  imports: [FormField],
  template: `
    <input type="email" [formField]="loginForm.email" />
    <input type="password" [formField]="loginForm.password" />
  `,
})
export class LoginComponent {
  loginModel = signal({
    email: '',
    password: '',
  });

  loginForm = form(this.loginModel);
}
```

[`form()`](api/forms/signals/form) funksiyasi model signalini qabul qiladi va **maydonlar daraxtini** (field tree) — modelingiz shaklini aks ettiruvchi maxsus obyekt tuzilmasini yaratadi. Maydonlar daraxti ham navigatsiya qilinadigan (`loginForm.email` kabi nuqta belgisi orqali ichki maydonlarga murojaat qilish), ham chaqiriladigan (maydonni funksiya sifatida chaqirib, uning holatiga murojaat qilish) obyektdir.

`[formField]` direktivi har bir input elementini maydonlar daraxtidagi tegishli maydonga bogʻlaydi va UI bilan model oʻrtasida avtomatik ikki tomonlama sinxronlashni taʼminlaydi.

### Qoʻllab-quvvatlanadigan model tuzilmalari {#supported-model-structures}

Signal Forms maydonlar daraxtini modelingiz boʻylab yurib yaratadi. U yurib oʻtadigan obyektlar va massivlar (**strukturaviy qatlam**) oddiy JavaScript obyektlari va massivlari boʻlishi shart. **Barglardagi** (ichki maydonlari boʻlmagan pozitsiyalardagi) qiymatlar odatda primitivlar (satrlar, sonlar, boolean'lar) yoki `null` boʻladi. Native `date`, `month`, `time` va `week` input'lari `Date`'ni ham qabul qiladi, maxsus kontrollar esa oʻzlari tushunadigan istalgan qiymat turini qabul qilishi mumkin.

```ts {prefer, header: 'Plain structure'}
interface UserFormModel {
  name: string;
  birthday: Date | null;
  preferences: {
    theme: string;
    notifications: boolean;
  };
  tags: string[];
}

const userModel = signal<UserFormModel>({
  name: '',
  birthday: null,
  preferences: {
    theme: 'dark',
    notifications: true,
  },
  tags: [],
});
```

IMPORTANT: Klass nusxalari (instance), `Map` va `Set` **strukturaviy qatlamda qoʻllab-quvvatlanmaydi**, TypeScript ularni qabul qilsa ham. Signal Forms model shaklini ish vaqtida tekshirmaydi, shuning uchun freymvork bu qiymatlarni xato tashlamasdan qabul qiladi, keyin esa shaklga qarab turli yoʻllar bilan notoʻgʻri ishlaydi:

- **Klass nusxalari** birinchi yozishda oʻz prototipini yoʻqotadi, chunki Signal Forms yangilashda ota obyektlarni yuzaki (shallow) nusxalaydi. Shundan keyin metodlar, getter'lar va `instanceof` tekshiruvlari ishlamay qoladi.
- **Massivlar ichidagi kengaytirilmaydigan yoki muzlatilgan (frozen) obyektlar** Signal Forms qayta tartiblashlarda element identifikatsiyasini saqlash uchun kuzatuv simvolini biriktirganda xato tashlaydi.
- **`Map` va `Set`** boʻsh maydonlar daraxtini hosil qiladi, chunki Signal Forms ichki elementlarni `Object.keys` bilan sanab chiqadi.

Agar ilovangiz domen modellashtirish uchun klasslardan foydalansa, forma chegarasida ularni oddiy obyektlarga aylantiring. [Forma modeli va domen modeli oʻrtasida oʻgirish](guide/forms/signals/model-design#translating-between-form-model-and-domain-model) boʻlimiga qarang.

### TypeScript tiplaridan foydalanish {#using-typescript-types}

TypeScript obyekt literallaridan tiplarni oʻzi aniqlasa-da, aniq tiplarni belgilash kod sifatini yaxshilaydi va IntelliSense yordamini kuchaytiradi.

```ts
interface LoginData {
  email: string;
  password: string;
}

export class LoginComponent {
  loginModel = signal<LoginData>({
    email: '',
    password: '',
  });

  loginForm = form(this.loginModel);
}
```

Aniq tiplar bilan maydonlar daraxti toʻliq tip xavfsizligini taʼminlaydi. `loginForm.email`'ga murojaat `FieldTree<string>` sifatida tiplanadi, mavjud boʻlmagan xususiyatga murojaat qilishga urinish esa kompilyatsiya vaqtida xatoga olib keladi.

```ts
// TypeScript knows this is FieldTree<string>
const emailField = loginForm.email;

// TypeScript error: Property 'username' does not exist
const usernameField = loginForm.username;
```

### Barcha maydonlarni ishga tushirish {#initializing-all-fields}

Forma modellari maydonlar daraxtiga kiritmoqchi boʻlgan barcha maydonlar uchun boshlangʻich qiymatlar berishi kerak.

```ts {prefer}
// Good: All fields initialized
const userModel = signal({
  name: '',
  email: '',
  age: 0,
});
```

```ts {avoid}
// Avoid: Missing initial value
const userModel = signal({
  name: '',
  email: '',
  // age field is not defined - cannot access userForm.age
});
```

Ixtiyoriy maydonlar uchun ularni aniq ravishda boʻsh qiymatga yoki `null`'ga oʻrnating:

```ts
interface UserData {
  name: string;
  email: string;
  phoneNumber: string | null;
}

const userModel = signal<UserData>({
  name: '',
  email: '',
  phoneNumber: null,
});
```

HELPFUL: `<input type=text>` va `<textarea>` kabi native matn kontrollari `null`'ni qoʻllab-quvvatlamaydi, boʻsh qiymatni ifodalash uchun `''` dan foydalaning.

`undefined` qiymatiga oʻrnatilgan maydonlar maydonlar daraxtidan chiqarib tashlanadi. `{value: undefined}` modeli `{}` bilan bir xil ishlaydi — maydonga murojaat `FieldTree` oʻrniga `undefined` qaytaradi.

## Model qiymatlarini oʻqish {#reading-model-values}

Forma qiymatlariga ikki yoʻl bilan murojaat qilishingiz mumkin: bevosita model signalidan yoki alohida maydonlar orqali. Har bir yondashuv oʻz maqsadiga xizmat qiladi.

### Modeldan oʻqish {#reading-from-the-model}

Toʻliq forma maʼlumotlari kerak boʻlganda, masalan, formani yuborish vaqtida model signaliga murojaat qiling:

```ts
async onSubmit() {
  const formData = this.loginModel();
  console.log(formData.email, formData.password);

  // Send to server
  await this.authService.login(formData);
}
```

Model signali butun maʼlumotlar obyektini qaytaradi, bu uni formaning toʻliq holati bilan ishlaydigan amallar uchun ideal qiladi.

### Maydon holatidan oʻqish {#reading-from-field-state}

Maydonlar daraxtidagi har bir maydon — funksiya. Maydonni chaqirish maydon qiymati, validatsiya holati va oʻzaro aloqa holati uchun reaktiv signallarni oʻz ichiga olgan `FieldState` obyektini qaytaradi.

Shablonlarda yoki reaktiv hisob-kitoblarda alohida maydonlar bilan ishlaganda maydon holatiga murojaat qiling:

```angular-ts
@Component({
  template: `
    <p>Current email: {{ loginForm.email().value() }}</p>
    <p>Password length: {{ passwordLength() }}</p>
  `,
})
export class LoginComponent {
  loginModel = signal({email: '', password: ''});
  loginForm = form(this.loginModel);

  passwordLength = computed(() => {
    return this.loginForm.password().value().length;
  });
}
```

Maydon holati har bir maydon qiymati uchun reaktiv signallarni taqdim etadi, bu uni maydonga xos maʼlumotlarni koʻrsatish yoki hosilaviy holat yaratish uchun mos qiladi.

TIP: Maydon holati `value()`'dan tashqari yana koʻp signallarni oʻz ichiga oladi, masalan, validatsiya holati (valid, invalid, errors), oʻzaro aloqani kuzatish (touched, dirty) va koʻrinish (hidden, disabled).

Toʻliq maʼlumot uchun [Maydon holatini boshqarish qoʻllanmasiga](guide/forms/signals/field-state-management) qarang.

## Forma modellarini dasturiy ravishda yangilash {#updating-form-models-programmatically}

### Forma modellarini `set()` bilan almashtirish {#replacing-form-models-with-set}

Butun qiymatni almashtirish uchun forma modelida `set()`'dan foydalaning:

```ts
loadUserData() {
  this.userModel.set({
    name: 'Alice',
    email: 'alice@example.com',
    age: 30,
  });
}

resetForm() {
  this.userModel.set({
    name: '',
    email: '',
    age: 0,
  });
}
```

Bu yondashuv API'dan maʼlumot yuklash yoki butun formani qayta tiklashda yaxshi ishlaydi.

### Bitta maydonni `set()` yoki `update()` bilan bevosita yangilash {#update-a-single-field-directly-with-set-or-update}

Maydon holatini bevosita yangilash uchun alohida maydon qiymatlarida `set()`'dan foydalaning:

```ts
clearEmail() {
  this.userForm.email().value.set('');
}

incrementAge() {
  this.userForm.age().value.update(currentAge => currentAge + 1);
}
```

Bular "maydon darajasidagi yangilanishlar" deb ham ataladi. Ular avtomatik ravishda model signaliga tarqaladi va ikkalasini sinxron holda saqlaydi.

### Misol: API'dan maʼlumot yuklash {#example-loading-data-from-an-api}

Keng tarqalgan namuna maʼlumotlarni olib, modelni toʻldirishni oʻz ichiga oladi:

```ts
export class UserProfileComponent {
  userModel = signal({
    name: '',
    email: '',
    bio: '',
  });

  userForm = form(this.userModel);
  private userService = inject(UserService);

  ngOnInit() {
    this.loadUserProfile();
  }

  async loadUserProfile() {
    const userData = await this.userService.getUserProfile();
    this.userModel.set(userData);
  }
}
```

Model oʻzgarganda forma maydonlari avtomatik yangilanadi va olingan maʼlumotlarni qoʻshimcha kodsiz koʻrsatadi.

## Ikki tomonlama maʼlumot bogʻlash {#two-way-data-binding}

`[formField]` direktivi model, forma holati va UI oʻrtasida avtomatik ikki tomonlama sinxronlash yaratadi.

### Maʼlumotlar qanday oqadi {#how-data-flows}

Oʻzgarishlar ikki yoʻnalishda oqadi:

**Foydalanuvchi kiritishi → Model:**

1. Foydalanuvchi input elementiga matn kiritadi
2. `[formField]` direktivi oʻzgarishni aniqlaydi
3. Maydon holati yangilanadi
4. Model signali yangilanadi

**Dasturiy yangilanish → UI:**

1. Kod modelni `set()` yoki `update()` bilan yangilaydi
2. Model signali obunachilarni xabardor qiladi
3. Maydon holati yangilanadi
4. `[formField]` direktivi input elementini yangilaydi

Bu sinxronlash avtomatik sodir boʻladi. Model va UI'ni sinxron saqlash uchun obunalar yoki hodisa ishlov beruvchilarini yozmaysiz.

### Misol: Ikkala yoʻnalish {#example-both-directions}

```angular-ts
@Component({
  template: `
    <input type="text" [formField]="userForm.name" />
    <button (click)="setName('Bob')">Set Name to Bob</button>
    <p>Current name: {{ userModel().name }}</p>
  `,
})
export class UserComponent {
  userModel = signal({name: ''});
  userForm = form(this.userModel);

  setName(name: string) {
    this.userForm.name().value.set(name);
    // Input automatically displays 'Bob'
  }
}
```

Foydalanuvchi input'ga matn kiritganda `userModel().name` yangilanadi. Tugma bosilganda input qiymati "Bob" ga oʻzgaradi. Hech qanday qoʻlda sinxronlash kodi talab qilinmaydi.

## Model tuzilmasi namunalari {#model-structure-patterns}

Forma modellari yassi (flat) obyektlar boʻlishi yoki ichki (nested) obyektlar va massivlarni oʻz ichiga olishi mumkin. Tanlagan tuzilmangiz maydonlarga qanday murojaat qilishingiz va validatsiyani qanday tashkil qilishingizga taʼsir qiladi.

### Yassi va ichki modellar {#flat-vs-nested-models}

Yassi forma modellari barcha maydonlarni yuqori darajada saqlaydi:

```ts
// Flat structure
const userModel = signal({
  name: '',
  email: '',
  street: '',
  city: '',
  state: '',
  zip: '',
});
```

Ichki modellar bogʻliq maydonlarni guruhlaydi:

```ts
// Nested structure
const userModel = signal({
  name: '',
  email: '',
  address: {
    street: '',
    city: '',
    state: '',
    zip: '',
  },
});
```

**Yassi tuzilmalardan quyidagi hollarda foydalaning:**

- Maydonlarning aniq konseptual guruhlari boʻlmasa
- Maydonlarga soddaroq murojaat qilishni istasangiz (`userForm.city` va `userForm.address.city`)
- Validatsiya qoidalari bir nechta potensial guruhni qamrab olsa

**Ichki tuzilmalardan quyidagi hollarda foydalaning:**

- Maydonlar aniq konseptual guruhni tashkil qilsa (manzil kabi)
- Guruhlangan maʼlumotlar API tuzilmangizga mos kelsa
- Guruhni yaxlit birlik sifatida tekshirishni istasangiz

### Ichki obyektlar bilan ishlash {#working-with-nested-objects}

Ichki maydonlarga obyekt yoʻli boʻylab murojaat qilishingiz mumkin:

```ts
const userModel = signal({
  profile: {
    firstName: '',
    lastName: '',
  },
  settings: {
    theme: 'light',
    notifications: true,
  },
});

const userForm = form(userModel);

// Access nested fields
userForm.profile.firstName; // FieldTree<string>
userForm.settings.theme; // FieldTree<string>
```

Shablonlarda ichki maydonlarni yuqori darajadagi maydonlar bilan bir xil tarzda bogʻlaysiz:

```angular-ts
@Component({
  template: `
    <input [formField]="userForm.profile.firstName" />
    <input [formField]="userForm.profile.lastName" />

    <select [formField]="userForm.settings.theme">
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  `,
})
```

### Massivlar bilan ishlash {#working-with-arrays}

Modellar elementlar toʻplami uchun massivlarni oʻz ichiga olishi mumkin:

```ts
const orderModel = signal({
  customerName: '',
  items: [{product: '', quantity: 0, price: 0}],
});

const orderForm = form(orderModel);

// Access array items by index
orderForm.items[0].product; // FieldTree<string>
orderForm.items[0].quantity; // FieldTree<number>
```

Obyektlardan iborat massiv elementlari avtomatik ravishda kuzatuv identifikatsiyalarini oladi, bu elementlar massivdagi oʻrnini oʻzgartirganda ham maydon holatini saqlab qolishga yordam beradi. Bu massivlar qayta tartiblanganda validatsiya holati va foydalanuvchi oʻzaro aloqalarining toʻgʻri saqlanishini taʼminlaydi.

<!-- TBD: For dynamic arrays and complex array operations, see the [Working with arrays guide](guide/forms/signals/arrays). -->

## Keyingi qadamlar {#next-steps}

Ushbu qoʻllanma modellar yaratish va qiymatlarni yangilashni yoritdi. Tegishli qoʻllanmalar Signal Forms'ning boshqa jihatlarini koʻrib chiqadi:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/custom-controls" title="Maxsus boshqaruv elementlari" />
  <!-- <docs-pill href="guide/forms/signals/arrays" title="Working with Arrays" /> -->
</docs-pill-row>
