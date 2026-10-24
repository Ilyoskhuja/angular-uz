# Boshqa forma yondashuvlari bilan taqqoslash

Angular formalar yaratishning uchta yondashuvini taqdim etadi: Signal Forms, reaktiv formalar (Reactive Forms) va shablonga asoslangan formalar (Template-driven Forms). Har birining holatni boshqarish, validatsiya va maʼlumotlar oqimi uchun oʻziga xos namunalari bor. Ushbu qoʻllanma farqlarni tushunishga va loyihangiz uchun toʻgʻri yondashuvni tanlashga yordam beradi.

## Qisqacha taqqoslash {#quick-comparison}

| Xususiyat           | Signal Forms                                    | Reaktiv formalar                                 | Shablonga asoslangan formalar      |
| ------------------- | ----------------------------------------------- | ------------------------------------------------ | ---------------------------------- |
| Haqiqat manbai      | Foydalanuvchi aniqlagan yozuvchan signal modeli | `FormControl`/`FormGroup`                        | Komponentdagi foydalanuvchi modeli |
| Tip xavfsizligi     | Modeldan chiqariladi                            | Tiplangan formalar bilan aniq                    | Minimal                            |
| Validatsiya         | Yoʻlga asoslangan validatorli sxema             | Control'larga uzatiladigan validatorlar roʻyxati | Direktivaga asoslangan             |
| Holatni boshqarish  | Signalga asoslangan                             | Observable'ga asoslangan                         | Angular tomonidan boshqariladi     |
| Sozlash             | Signal + sxema funksiyasi                       | FormControl daraxti                              | Shablonda NgModel                  |
| Eng mos             | Signalga asoslangan ilovalar                    | Murakkab formalar                                | Oddiy formalar                     |
| Oʻrganish qiyinligi | Oʻrta                                           | Oʻrta-yuqori                                     | Past                               |
| Holat               | Barqaror (v22+)                                 | Barqaror                                         | Barqaror                           |

## Misol orqali: Kirish formasi {#by-example-login-form}

Farqlarni tushunishning eng yaxshi usuli - bir xil formani uchala yondashuvda amalga oshirilgan holda koʻrish.

<docs-code-multifile>
  <docs-code language="angular-ts" header="Signal forms" path="adev/src/content/examples/signal-forms/src/comparison/app/signal-forms.ts"/>
  <docs-code header="Reactive forms" path="adev/src/content/examples/signal-forms/src/comparison/app/reactive-forms.ts"/>
  <docs-code header="Template-driven forms" path="adev/src/content/examples/signal-forms/src/comparison/app/template-driven-forms.ts"/>
</docs-code-multifile>

## Farqlarni tushunish {#understanding-the-differences}

Uchta yondashuv formalaringizni qanday yozishingiz va qoʻllab-quvvatlashingizga taʼsir qiluvchi turli dizayn qarorlarini qabul qiladi. Bu farqlar har bir yondashuvning forma holatini qayerda saqlashi va validatsiyani qanday boshqarishidan kelib chiqadi.

### Forma maʼlumotlaringiz qayerda saqlanadi {#where-your-form-data-lives}

Eng tub farq - har bir yondashuv forma qiymatlari uchun "haqiqat manbai"ni (source of truth) qayerda deb hisoblashida.

Signal Forms maʼlumotlarni yozuvchan signalda saqlaydi. Joriy forma qiymatlari kerak boʻlganda signalni chaqirasiz:

```ts
const credentials = this.loginModel(); // { email: '...', password: '...' }
```

Bu forma maʼlumotlaringizni qiymatlar oʻzgarganda Angular'ni avtomatik xabardor qiladigan yagona reaktiv konteynerda saqlaydi. Forma tuzilmasi maʼlumotlar modelingizni aynan aks ettiradi.

Reaktiv formalar maʼlumotlarni FormControl va FormGroup nusxalari ichida saqlaydi. Qiymatlarga forma ierarxiyasi orqali murojaat qilasiz:

```ts
const credentials = this.loginForm.value; // { email: '...', password: '...' }
```

Bu forma holatini boshqarishni komponentingizning maʼlumotlar modelidan ajratadi. Forma tuzilmasi aniq, lekin koʻproq sozlash kodini talab qiladi.

Shablonga asoslangan formalar maʼlumotlarni komponent xususiyatlarida saqlaydi. Qiymatlarga toʻgʻridan-toʻgʻri murojaat qilasiz:

```ts
const credentials = {email: this.email, password: this.password};
```

Bu eng bevosita yondashuv, lekin qiymatlar kerak boʻlganda ularni qoʻlda yigʻishni talab qiladi. Angular forma holatini shablondagi direktivalar orqali boshqaradi.

### Validatsiya qanday ishlaydi {#how-validation-works}

Har bir yondashuv validatsiya qoidalarini turlicha aniqlaydi, bu validatsiya mantigʻingiz qayerda joylashishi va uni qanday qoʻllab-quvvatlashingizga taʼsir qiladi.

Signal Forms validatorlarni maydon yoʻllariga bogʻlaydigan sxema funksiyasidan foydalanadi:

```ts
loginForm = form(this.loginModel, (fieldPath) => {
  required(fieldPath.email, {message: 'Email is required'});
  email(fieldPath.email, {message: 'Enter a valid email address'});
});
```

Barcha validatsiya qoidalari bir joyda birga joylashadi. Sxema funksiyasi forma yaratilayotganda bir marta bajariladi va validatorlar maydon qiymatlari oʻzgarganda avtomatik ishga tushadi. Xato xabarlari validatsiya taʼrifining bir qismidir.

Reaktiv formalar validatorlarni control'lar yaratilayotganda biriktiradi:

```ts
loginForm = new FormGroup({
  email: new FormControl('', [Validators.required, Validators.email]),
});
```

Validatorlar forma tuzilmasidagi alohida control'larga bogʻlangan. Bu validatsiyani forma taʼrifi boʻylab taqsimlaydi. Xato xabarlari odatda shablonigizda joylashadi.

Shablonga asoslangan formalar shablondagi direktiva atributlaridan foydalanadi:

```html
<input [(ngModel)]="email" required email />
```

Validatsiya qoidalari shablonigizda HTML bilan yonma-yon joylashadi. Bu validatsiyani UI'ga yaqin saqlaydi, lekin mantiqni shablon va komponent oʻrtasida tarqatib yuboradi.

### Tip xavfsizligi va avtotoʻldirish {#type-safety-and-autocomplete}

TypeScript integratsiyasi yondashuvlar oʻrtasida sezilarli farq qiladi va kompilyator xatolardan qochishingizga qanchalik yordam berishiga taʼsir qiladi.

Signal Forms tiplarni model tuzilmangizdan chiqaradi:

```ts
const loginModel = signal({email: '', password: ''});
const loginForm = form(loginModel);
// TypeScript knows: loginForm.email exists and returns FieldState<string>
```

Maʼlumotlar shaklini signalda bir marta aniqlaysiz va TypeScript qanday maydonlar mavjudligini va ularning tiplarini avtomatik biladi. `loginForm.username`'ga (mavjud boʻlmagan maydon) murojaat qilish tip xatosini keltirib chiqaradi.

Reaktiv formalar tiplangan formalar bilan aniq tip annotatsiyalarini talab qiladi:

```ts
const loginForm = new FormGroup({
  email: new FormControl<string>(''),
  password: new FormControl<string>(''),
});
// TypeScript knows: loginForm.controls.email is FormControl<string>
```

Har bir control uchun tiplarni alohida koʻrsatasiz. TypeScript forma tuzilmangizni tekshiradi, lekin tip maʼlumotlarini maʼlumotlar modelingizdan alohida qoʻllab-quvvatlaysiz.

Shablonga asoslangan formalar minimal tip xavfsizligini taqdim etadi:

```ts
email = '';
password = '';
// TypeScript only knows these are strings, no form-level typing
```

TypeScript komponent xususiyatlaringizni tushunadi, lekin forma tuzilmasi yoki validatsiya haqida hech narsa bilmaydi. Forma amallari uchun kompilyatsiya vaqtidagi tekshiruvdan mahrum boʻlasiz.

## Yondashuvingizni tanlang {#choose-your-approach}

### Signal Forms'dan foydalaning, agar: {#use-signal-forms-if}

- Yangi, signalga asoslangan ilovalar yaratayotgan boʻlsangiz (Angular v22+)
- Model tuzilmangizdan chiqariladigan tip xavfsizligini istasangiz
- Sxemaga asoslangan validatsiya sizga yoqsa
- Jamoangiz signallar bilan tanish boʻlsa

### Reaktiv formalardan foydalaning, agar: {#use-reactive-forms-if}

- Production uchun tayyor barqarorlik kerak boʻlsa
- Murakkab, dinamik formalar yaratayotgan boʻlsangiz
- Observable'ga asoslangan namunalarni afzal koʻrsangiz
- Forma holati ustidan nozik boshqaruv kerak boʻlsa
- Mavjud reaktiv formalar kod bazasi ustida ishlayotgan boʻlsangiz

### Shablonga asoslangan formalardan foydalaning, agar: {#use-template-driven-forms-if}

- Oddiy formalar (kirish, aloqa, qidiruv) yaratayotgan boʻlsangiz
- Tez prototip yaratayotgan boʻlsangiz
- Forma mantigʻingiz sodda boʻlsa
- Forma mantigʻini shablonlarda saqlashni afzal koʻrsangiz
- Mavjud shablonga asoslangan kod bazasi ustida ishlayotgan boʻlsangiz

## Keyingi qadamlar {#next-steps}

Har bir yondashuv haqida koʻproq bilish uchun:

- **Signal Forms**: Boshlash uchun [Umumiy koʻrinish qoʻllanmasiga](guide/forms/signals/overview) qarang yoki [Forma modellari](guide/forms/signals/models), [Validatsiya](guide/forms/signals/validation) va [Maydon holatini boshqarish](guide/forms/signals/field-state-management) boʻlimlariga chuqurroq kiring
- **Reaktiv formalar**: Angular hujjatlaridagi [Reaktiv formalar qoʻllanmasiga](guide/forms/reactive-forms) qarang
- **Shablonga asoslangan formalar**: Angular hujjatlaridagi [Shablonga asoslangan formalar qoʻllanmasiga](guide/forms/template-driven-forms) qarang
