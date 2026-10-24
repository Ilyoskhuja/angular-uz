# Tiplangan formalar

Angular 14 dan boshlab reaktiv formalar sukut boʻyicha qatʼiy tiplangan.

Bu qoʻllanmani oʻqishdan oldin siz [Angular reaktiv formalari](guide/forms/reactive-forms) bilan tanish boʻlishingiz kerak.

## Tiplangan formalarning umumiy koʻrinishi {#overview-of-typed-forms}

<docs-video src="https://www.youtube.com/embed/L-odCf4MfJc" title="Angular'da tiplangan formalar" />

Angular reaktiv formalarida siz _forma modelini_ aniq koʻrsatasiz. Oddiy misol sifatida quyidagi asosiy foydalanuvchi kirish formasini koʻrib chiqing:

```ts
const login = new FormGroup({
  email: new FormControl(''),
  password: new FormControl(''),
});
```

Angular bu `FormGroup` bilan ishlash uchun koʻplab API'lar taqdim etadi. Masalan, siz `login.value`, `login.controls`, `login.patchValue` va shu kabilarni chaqirishingiz mumkin. (Toʻliq API maʼlumotnomasi uchun [API hujjatlariga](api/forms/FormGroup) qarang.)

Angular'ning oldingi versiyalarida bu API'larning aksariyati oʻz tiplarida qayerdadir `any` ni oʻz ichiga olar edi va boshqaruv elementlarining tuzilmasi yoki qiymatlarning oʻzi bilan ishlash tip jihatidan xavfsiz emas edi. Masalan, siz quyidagi notoʻgʻri kodni yozishingiz mumkin edi:

```ts
const emailDomain = login.value.email.domain;
```

Qatʼiy tiplangan reaktiv formalarda yuqoridagi kod kompilyatsiya qilinmaydi, chunki `email` da `domain` xususiyati yoʻq.

Qoʻshimcha xavfsizlikdan tashqari, tiplar IDE'larda yaxshiroq avtotoʻldirish va forma tuzilmasini aniq koʻrsatish usuli kabi boshqa bir qator yaxshilanishlarni ham taʼminlaydi.

Bu yaxshilanishlar hozircha faqat _reaktiv_ formalarga tegishli ([_shablonga asoslangan_ formalarga](guide/forms/template-driven-forms) emas).

## Tiplanmagan formalar {#untyped-forms}

Tiplanmagan formalar hali ham qoʻllab-quvvatlanadi va avvalgidek ishlashda davom etadi. Ulardan foydalanish uchun `@angular/forms` dan `Untyped` simvollarini import qilishingiz kerak:

```ts
const login = new UntypedFormGroup({
  email: new UntypedFormControl(''),
  password: new UntypedFormControl(''),
});
```

Har bir `Untyped` simvoli Angular'ning oldingi versiyalaridagi bilan aynan bir xil semantikaga ega. `Untyped` prefikslarini olib tashlash orqali tiplarni bosqichma-bosqich yoqishingiz mumkin.

## `FormControl`: ishni boshlash {#formcontrol-getting-started}

Mumkin boʻlgan eng sodda forma bitta boshqaruv elementidan iborat:

```ts
const email = new FormControl('angularrox@gmail.com');
```

Bu boshqaruv elementining tipi avtomatik ravishda `FormControl<string|null>` sifatida aniqlanadi. TypeScript bu tipni [`FormControl` API'sining](api/forms/FormControl) butun doirasida, masalan `email.value`, `email.valueChanges` va `email.setValue(...)` da avtomatik ravishda talab qiladi.

### Null boʻlishi mumkinligi {#nullability}

Siz hayron boʻlishingiz mumkin: nega bu boshqaruv elementining tipi `null` ni oʻz ichiga oladi? Chunki boshqaruv elementi reset chaqirilganda istalgan vaqtda `null` boʻlib qolishi mumkin:

```ts
const email = new FormControl('angularrox@gmail.com');
email.reset();
console.log(email.value); // null
```

TypeScript boshqaruv elementi `null` boʻlib qolgan boʻlishi ehtimolini har doim hisobga olishingizni talab qiladi. Agar bu boshqaruv elementini null boʻlmaydigan qilmoqchi boʻlsangiz, `nonNullable` opsiyasidan foydalanishingiz mumkin. Bu boshqaruv elementining `null` oʻrniga oʻz boshlangʻich qiymatiga qaytarilishiga olib keladi:

```ts
const email = new FormControl('angularrox@gmail.com', {nonNullable: true});
email.reset();
console.log(email.value); // angularrox@gmail.com
```

Yana bir bor takrorlaymiz: bu opsiya `.reset()` chaqirilganda formangizning ish vaqtidagi xatti-harakatiga taʼsir qiladi va uni ehtiyotkorlik bilan oʻzgartirish kerak.

### Tipni aniq koʻrsatish {#specifying-an-explicit-type}

Tipni avtomatik aniqlashga tayanish oʻrniga uni aniq koʻrsatish mumkin. `null` bilan ishga tushirilgan boshqaruv elementini koʻrib chiqing. Boshlangʻich qiymat `null` boʻlgani uchun TypeScript `FormControl<null>` deb aniqlaydi, bu esa biz istaganimizdan torroq.

```ts
const email = new FormControl(null);
email.setValue('angularrox@gmail.com'); // Error!
```

Bunga yoʻl qoʻymaslik uchun tipni aniq ravishda `string|null` sifatida koʻrsatamiz:

```ts
const email = new FormControl<string | null>(null);
email.setValue('angularrox@gmail.com');
```

## `FormArray`: dinamik, bir jinsli toʻplamlar {#formarray-dynamic-homogenous-collections}

`FormArray` boshqaruv elementlarining cheklanmagan roʻyxatini oʻz ichiga oladi. Tip parametri har bir ichki boshqaruv elementining tipiga mos keladi:

```ts
const names = new FormArray([new FormControl('Alex')]);
names.push(new FormControl('Jess'));
```

Bir vaqtning oʻzida bir nechta element qoʻshish kerak boʻlganda `aliases.push()` ga boshqaruv elementlari massivini uzating.

```ts
const aliases = new FormArray([new FormControl('ng')]);
aliases.push([new FormControl('ngDev'), new FormControl('ngAwesome')]);
```

Bu `FormArray` ning ichki boshqaruv elementlari tipi `FormControl<string|null>` boʻladi.

Agar massiv ichida bir nechta turli element tiplari boʻlishini istasangiz, `UntypedFormArray` dan foydalanishingiz kerak, chunki TypeScript qaysi element tipi qaysi pozitsiyada boʻlishini aniqlay olmaydi.

`FormArray` shuningdek, oʻz ichidagi barcha boshqaruv elementlarini olib tashlash uchun `clear()` metodini ham taqdim etadi:

```ts
const aliases = new FormArray([new FormControl('ngDev'), new FormControl('ngAwesome')]);
aliases.clear();
console.log(aliases.length); // 0
```

## `FormGroup` va `FormRecord` {#formgroup-and-formrecord}

Angular kalitlari sanab oʻtilgan formalar uchun `FormGroup` tipini, cheklanmagan yoki dinamik guruhlar uchun esa `FormRecord` deb nomlangan tipni taqdim etadi.

### Qismiy qiymatlar {#partial-values}

Kirish formasini yana bir bor koʻrib chiqing:

```ts
const login = new FormGroup({
  email: new FormControl('', {nonNullable: true}),
  password: new FormControl('', {nonNullable: true}),
});
```

Har qanday `FormGroup` da [boshqaruv elementlarini oʻchirib qoʻyish mumkin](api/forms/FormGroup). Oʻchirib qoʻyilgan har qanday boshqaruv elementi guruh qiymatida koʻrinmaydi.

Natijada `login.value` ning tipi `Partial<{email: string, password: string}>` boʻladi. Bu tipdagi `Partial` har bir aʼzo undefined boʻlishi mumkinligini bildiradi.

Aniqroq aytganda, `login.value.email` ning tipi `string|undefined` boʻladi va TypeScript `undefined` boʻlishi mumkin boʻlgan qiymatni hisobga olishingizni talab qiladi (agar `strictNullChecks` yoqilgan boʻlsa).

Agar qiymatga oʻchirib qoʻyilgan boshqaruv elementlarini _ham qoʻshib_ murojaat qilmoqchi boʻlsangiz va shu tariqa `undefined` boʻlishi mumkin boʻlgan maydonlarni chetlab oʻtmoqchi boʻlsangiz, `login.getRawValue()` dan foydalanishingiz mumkin.

### Ixtiyoriy boshqaruv elementlari va dinamik guruhlar {#optional-controls-and-dynamic-groups}

Baʼzi formalarda mavjud boʻlishi ham, boʻlmasligi ham mumkin boʻlgan, ish vaqtida qoʻshilishi va olib tashlanishi mumkin boʻlgan boshqaruv elementlari bor. Bunday boshqaruv elementlarini _ixtiyoriy maydonlar_ yordamida ifodalashingiz mumkin:

```ts
interface LoginForm {
  email: FormControl<string>;
  password?: FormControl<string>;
}

const login = new FormGroup<LoginForm>({
  email: new FormControl('', {nonNullable: true}),
  password: new FormControl('', {nonNullable: true}),
});

login.removeControl('password');
```

Bu formada biz tipni aniq koʻrsatamiz, bu esa `password` boshqaruv elementini ixtiyoriy qilish imkonini beradi. TypeScript faqat ixtiyoriy boshqaruv elementlarini qoʻshish yoki olib tashlash mumkinligini talab qiladi.

### `FormRecord`

`FormGroup` dan foydalanishning baʼzi holatlari yuqoridagi namunaga mos kelmaydi, chunki kalitlar oldindan maʼlum boʻlmaydi. `FormRecord` klassi aynan shu holat uchun moʻljallangan:

```ts
const addresses = new FormRecord<FormControl<string | null>>({});
addresses.addControl('Andrew', new FormControl('2340 Folsom St'));
```

Bu `FormRecord` ga `string|null` tipidagi har qanday boshqaruv elementini qoʻshish mumkin.

Agar sizga bir vaqtning oʻzida dinamik (cheklanmagan) ham, bir jinsli boʻlmagan (boshqaruv elementlari turli tiplarda) ham `FormGroup` kerak boʻlsa, tip xavfsizligini yaxshilash imkoni yoʻq va siz `UntypedFormGroup` dan foydalanishingiz kerak.

`FormRecord` ni `FormBuilder` yordamida ham yaratish mumkin:

```ts
const addresses = fb.record({'Andrew': '2340 Folsom St'});
```

## `FormBuilder` va `NonNullableFormBuilder` {#formbuilder-and-nonnullableformbuilder}

`FormBuilder` klassi ham yuqoridagi misollardagi kabi yangi tiplarni qoʻllab-quvvatlash uchun yangilandi.

Bundan tashqari, yana bir builder mavjud: `NonNullableFormBuilder`. Bu tip har bir boshqaruv elementida `{nonNullable: true}` ni koʻrsatishning qisqa shakli boʻlib, katta null boʻlmaydigan formalarda koʻp miqdordagi shablon koddan (boilerplate) qutulish imkonini beradi. Unga `FormBuilder` dagi `nonNullable` xususiyati orqali murojaat qilishingiz mumkin:

```ts
const fb = new FormBuilder();
const login = fb.nonNullable.group({
  email: '',
  password: '',
});
```

Yuqoridagi misolda ikkala ichki boshqaruv elementi ham null boʻlmaydigan boʻladi (yaʼni `nonNullable` oʻrnatiladi).

Shuningdek, uni `NonNullableFormBuilder` nomi bilan inyeksiya qilishingiz ham mumkin.
