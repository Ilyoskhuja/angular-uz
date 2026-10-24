# Forma kiritmalarini validatsiya qilish

Foydalanuvchi kiritmalarini toʻgʻrilik va toʻliqlik boʻyicha validatsiya qilish orqali maʼlumotlarning umumiy sifatini yaxshilashingiz mumkin.
Ushbu sahifa reaktiv formalarda ham, shablonga asoslangan formalarda ham UI'dan kelgan foydalanuvchi kiritmalarini qanday validatsiya qilish va foydali validatsiya xabarlarini koʻrsatishni tushuntiradi.

## Shablonga asoslangan formalarda kiritmani validatsiya qilish {#validating-input-in-template-driven-forms}

Shablonga asoslangan formaga validatsiya qoʻshish uchun [HTML'ning oʻz forma validatsiyasida](https://developer.mozilla.org/docs/Web/Guide/HTML/HTML5/Constraint_validation) qoʻshadigan validatsiya atributlarining oʻzini qoʻshasiz.
Angular bu atributlarni freymvorkdagi validator funksiyalari bilan moslashtirish uchun direktivalardan foydalanadi.

Forma kontrolining qiymati har safar oʻzgarganda Angular validatsiyani ishga tushiradi va yo `INVALID` holatiga olib keluvchi validatsiya xatolari roʻyxatini, yo `VALID` holatiga olib keluvchi `null` qiymatini hosil qiladi.

Keyin `ngModel`'ni lokal shablon oʻzgaruvchisiga eksport qilib, kontrol holatini tekshirishingiz mumkin.
Quyidagi misol `NgModel`'ni `name` nomli oʻzgaruvchiga eksport qiladi:

<docs-code header="actor-form-template.component.html (name)" path="adev/src/content/examples/form-validation/src/app/template/actor-form-template.component.html" region="name-with-error-msg"/>

Misolda koʻrsatilgan quyidagi xususiyatlarga eʼtibor bering.

- `<input>` elementi HTML validatsiya atributlarini oʻz ichiga oladi: `required` va `minlength`.
  Shuningdek, u `forbiddenName` nomli maxsus validator direktivasini ham oʻz ichiga oladi.
  Koʻproq maʼlumot uchun [Maxsus validatorlar](#defining-custom-validators) boʻlimiga qarang.

- `#name="ngModel"` `NgModel`'ni `name` nomli lokal oʻzgaruvchiga eksport qiladi.
  `NgModel` oʻzining asosidagi `FormControl` nusxasining koʻplab xususiyatlarini aks ettiradi, shuning uchun shablonda `valid` va `dirty` kabi kontrol holatlarini tekshirish uchun undan foydalanishingiz mumkin.
  Kontrol xususiyatlarining toʻliq roʻyxati uchun [AbstractControl](api/forms/AbstractControl) API maʼlumotnomasiga qarang.
  - Eng tashqi `@if` ichki xabarlar toʻplamini faqat `name` notoʻgʻri (invalid) va kontrol `dirty` yoki `touched` boʻlgan holda koʻrsatadi.

  - Har bir ichki `@if` mumkin boʻlgan validatsiya xatolaridan biri uchun maxsus xabar koʻrsatishi mumkin.
    `required`, `minlength` va `forbiddenName` uchun xabarlar mavjud.

HELPFUL: Foydalanuvchi formani tahrirlash imkoniga ega boʻlishidan oldin validator xatolarni koʻrsatishining oldini olish uchun kontrolda `dirty` yoki `touched` holatlaridan birini tekshirishingiz kerak.

- Foydalanuvchi kuzatilayotgan maydondagi qiymatni oʻzgartirganda kontrol "dirty" deb belgilanadi
- Foydalanuvchi forma kontroli elementidan fokusni olib tashlaganda (blur) kontrol "touched" deb belgilanadi

## Reaktiv formalarda kiritmani validatsiya qilish {#validating-input-in-reactive-forms}

Reaktiv formada haqiqat manbai (source of truth) komponent klassidir.
Validatorlarni shablondagi atributlar orqali qoʻshish oʻrniga, validator funksiyalarini toʻgʻridan-toʻgʻri komponent klassidagi forma kontroli modeliga qoʻshasiz.
Keyin Angular kontrol qiymati oʻzgarganda bu funksiyalarni chaqiradi.

### Validator funksiyalari {#validator-functions}

Validator funksiyalari sinxron yoki asinxron boʻlishi mumkin.

| Validator turi        | Tafsilotlar                                                                                                                                                                                                                       |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sinxron validatorlar  | Kontrol nusxasini qabul qilib, darhol validatsiya xatolari toʻplamini yoki `null` qaytaradigan sinxron funksiyalar. `FormControl` yaratishda ularni ikkinchi argument sifatida uzating.                                           |
| Asinxron validatorlar | Kontrol nusxasini qabul qilib, keyinroq validatsiya xatolari toʻplamini yoki `null` chiqaradigan Promise yoki Observable qaytaradigan asinxron funksiyalar. `FormControl` yaratishda ularni uchinchi argument sifatida uzating. |

Samaradorlik sabablariga koʻra Angular asinxron validatorlarni faqat barcha sinxron validatorlar muvaffaqiyatli oʻtganda ishga tushiradi.
Xatolar oʻrnatilishidan oldin har biri yakunlanishi kerak.

### Oʻrnatilgan validator funksiyalari {#built-in-validator-functions}

[Oʻz validator funksiyalaringizni yozishni](#defining-custom-validators) tanlashingiz yoki Angular'ning oʻrnatilgan validatorlaridan foydalanishingiz mumkin.

Shablonga asoslangan formalarda atributlar sifatida mavjud boʻlgan `required` va `minlength` kabi oʻrnatilgan validatorlarning barchasi `Validators` klassidan funksiyalar sifatida foydalanish uchun mavjud.
Oʻrnatilgan validatorlarning toʻliq roʻyxati uchun [Validators](api/forms/Validators) API maʼlumotnomasiga qarang.

Aktyor formasini reaktiv formaga aylantirish uchun xuddi shu oʻrnatilgan validatorlardan
— bu safar funksiya koʻrinishida — quyidagi misoldagidek foydalaning.

<docs-code header="actor-form-reactive.component.ts (validator funksiyalari)" path="adev/src/content/examples/form-validation/src/app/reactive/actor-form-reactive.component.1.ts" region="form-group"/>

Bu misolda `name` kontroli ikkita oʻrnatilgan validator — `Validators.required` va `Validators.minLength(4)` — hamda bitta maxsus validator `forbiddenNameValidator`'ni oʻrnatadi.

Bu validatorlarning barchasi sinxron, shuning uchun ular ikkinchi argument sifatida uzatiladi.
Funksiyalarni massiv sifatida uzatish orqali bir nechta validatorni qoʻllab-quvvatlashingiz mumkinligiga eʼtibor bering.

Bu misol shuningdek bir nechta getter metodlarini ham qoʻshadi.
Reaktiv formada istalgan forma kontroliga uning ota guruhidagi `get` metodi orqali har doim murojaat qilishingiz mumkin, lekin baʼzan shablon uchun qisqartma sifatida getter'lar aniqlash foydali boʻladi.

`name` input'i uchun shablonga yana qarasangiz, u shablonga asoslangan misolga ancha oʻxshash.

<docs-code header="actor-form-reactive.component.html (xato xabari bilan name)" path="adev/src/content/examples/form-validation/src/app/reactive/actor-form-reactive.component.html" region="name-with-error-msg"/>

Bu forma shablonga asoslangan versiyadan endi hech qanday direktiva eksport qilmasligi bilan farqlanadi. Buning oʻrniga u komponent klassida aniqlangan `name` getter'idan foydalanadi.

`required` atributi shablonda hali ham mavjudligiga eʼtibor bering. Validatsiya uchun zarur boʻlmasa-da, uni foydalanish qulayligi (accessibility) maqsadida saqlab qolish kerak.

## Maxsus validatorlarni aniqlash {#defining-custom-validators}

Oʻrnatilgan validatorlar har doim ham ilovangizning aniq ehtiyojiga mos kelmaydi, shuning uchun baʼzan maxsus validator yaratishingiz kerak boʻladi.

Oldingi misoldagi `forbiddenNameValidator` funksiyasini koʻrib chiqing.
Bu funksiyaning taʼrifi quyidagicha koʻrinadi.

<docs-code header="forbidden-name.directive.ts (forbiddenNameValidator)" path="adev/src/content/examples/form-validation/src/app/shared/forbidden-name.directive.ts" region="custom-validator"/>

Bu funksiya _maʼlum_ bir taqiqlangan nomni aniqlash uchun regulyar ifodani qabul qilib, validator funksiyasini qaytaradigan fabrikadir.

Bu namunada taqiqlangan nom "bob", shuning uchun validator "bob" soʻzini oʻz ichiga olgan har qanday aktyor nomini rad etadi.
Boshqa joyda u "alice"ni yoki sozlovchi regulyar ifodaga mos keladigan istalgan nomni rad etishi mumkin.

`forbiddenNameValidator` fabrikasi sozlangan validator funksiyasini qaytaradi.
Bu funksiya Angular kontrol obyektini qabul qiladi va kontrol qiymati toʻgʻri boʻlsa null, _aks holda_ validatsiya xatosi obyektini qaytaradi.
Validatsiya xatosi obyekti odatda nomi validatsiya kaliti `'forbiddenName'` boʻlgan va qiymati xato xabariga qoʻyishingiz mumkin boʻlgan ixtiyoriy qiymatlar lugʻati `{name}` boʻlgan xususiyatga ega.

Maxsus asinxron validatorlar sinxron validatorlarga oʻxshaydi, lekin ular keyinroq null yoki validatsiya xatosi obyektini chiqaradigan Promise yoki observable qaytarishi kerak.
Observable boʻlgan holda, observable yakunlanishi (complete) kerak, shu paytda forma validatsiya uchun chiqarilgan soʻnggi qiymatdan foydalanadi.

### Reaktiv formalarga maxsus validatorlarni qoʻshish {#adding-custom-validators-to-reactive-forms}

Reaktiv formalarda funksiyani toʻgʻridan-toʻgʻri `FormControl`'ga uzatish orqali maxsus validator qoʻshing.

<docs-code header="actor-form-reactive.component.ts (validator funksiyalari)" path="adev/src/content/examples/form-validation/src/app/reactive/actor-form-reactive.component.1.ts" region="custom-validator"/>

### Shablonga asoslangan formalarga maxsus validatorlarni qoʻshish {#adding-custom-validators-to-template-driven-forms}

Shablonga asoslangan formalarda shablonga validator funksiyasini oʻrab turuvchi direktiva qoʻshing.
Masalan, tegishli `ForbiddenValidatorDirective` `forbiddenNameValidator` atrofida oʻram vazifasini bajaradi.

Angular direktivaning validatsiya jarayonidagi rolini taniydi, chunki direktiva quyidagi misolda koʻrsatilganidek, oʻzini `NG_VALIDATORS` provider'ida roʻyxatdan oʻtkazadi.
`NG_VALIDATORS` kengaytiriladigan validatorlar toʻplamiga ega oldindan aniqlangan provider'dir.

<docs-code header="forbidden-name.directive.ts (provider'lar)" path="adev/src/content/examples/form-validation/src/app/shared/forbidden-name.directive.ts" region="directive-providers"/>

Keyin direktiva klassi Angular formalari bilan oson integratsiya qilishi uchun `Validator` interfeysini amalga oshiradi.
Hammasi qanday birlashishini tasavvur qilishingizga yordam berish uchun direktivaning qolgan qismi quyida keltirilgan.

<docs-code header="forbidden-name.directive.ts (direktiva)" path="adev/src/content/examples/form-validation/src/app/shared/forbidden-name.directive.ts" region="directive"/>

`ForbiddenValidatorDirective` tayyor boʻlgach, uni faollashtirish uchun uning selektori `appForbiddenName`'ni istalgan input elementiga qoʻshishingiz mumkin.
Masalan:

<docs-code header="actor-form-template.component.html (forbidden-name-input)" path="adev/src/content/examples/form-validation/src/app/template/actor-form-template.component.html" region="name-input"/>

HELPFUL: Maxsus validatsiya direktivasi `useClass` emas, `useExisting` bilan yaratilishiga eʼtibor bering.
Roʻyxatdan oʻtkazilgan validator `ForbiddenValidatorDirective`'ning _aynan shu nusxasi_ — formadagi `forbiddenName` xususiyati "bob"ga bogʻlangan nusxa boʻlishi kerak.

Agar `useExisting`'ni `useClass` bilan almashtirsangiz, `forbiddenName`'ga ega boʻlmagan yangi klass nusxasini roʻyxatdan oʻtkazgan boʻlar edingiz.

## Kontrol holati CSS klasslari {#control-status-css-classes}

Angular koʻplab kontrol xususiyatlarini forma kontroli elementiga CSS klasslari sifatida avtomatik aks ettiradi.
Forma holatiga qarab forma kontroli elementlariga stil berish uchun bu klasslardan foydalaning.
Hozirda quyidagi klasslar qoʻllab-quvvatlanadi.

- `.ng-valid`
- `.ng-invalid`
- `.ng-pending`
- `.ng-pristine`
- `.ng-dirty`
- `.ng-untouched`
- `.ng-touched`
- `.ng-submitted` \(faqat oʻrab turuvchi forma elementi\)

Quyidagi misolda aktyor formasi har bir forma kontroli chegarasining rangini oʻrnatish uchun
`.ng-valid` va `.ng-invalid` klasslaridan foydalanadi.

<docs-code header="forms.css (holat klasslari)" path="adev/src/content/examples/form-validation/src/assets/forms.css"/>

## Maydonlararo validatsiya {#cross-field-validation}

Maydonlararo validator — bu formadagi turli maydonlarning qiymatlarini solishtirib, ularni birgalikda qabul qiladigan yoki rad etadigan [maxsus validator](#defining-custom-validators 'Maxsus validatorlar haqida oʻqing').
Masalan, sizda bir-biriga mos kelmaydigan variantlarni taklif qiladigan forma boʻlishi mumkin, shunda foydalanuvchi A yoki B ni tanlashi mumkin, lekin ikkalasini birga emas.
Baʼzi maydon qiymatlari boshqalariga bogʻliq boʻlishi ham mumkin; foydalanuvchiga B ni tanlashga faqat A ham tanlangan boʻlsa ruxsat berilishi mumkin.

Quyidagi maydonlararo validatsiya misollari quyidagilarni qanday bajarishni koʻrsatadi:

- Ikki qoʻshni kontrolning qiymatlariga asoslanib reaktiv yoki shablonga asoslangan forma kiritmasini validatsiya qilish,
- Foydalanuvchi forma bilan oʻzaro aloqa qilib, validatsiya muvaffaqiyatsiz boʻlgandan keyin tushunarli xato xabarini koʻrsatish.

Misollar aktyorlar Aktyor formasini toʻldirishda rollarida bir xil nomdan qayta foydalanmasligini taʼminlash uchun maydonlararo validatsiyadan foydalanadi.
Validatorlar buni aktyor nomlari va rollari mos kelmasligini tekshirish orqali amalga oshiradi.

### Reaktiv formalarga maydonlararo validatsiya qoʻshish {#adding-cross-validation-to-reactive-forms}

Forma quyidagi tuzilmaga ega:

```ts
const actorForm = new FormGroup({
  'name': new FormControl(),
  'role': new FormControl(),
  'skill': new FormControl(),
});
```

`name` va `role` qoʻshni kontrollar ekanligiga eʼtibor bering.
Ikkala kontrolni bitta maxsus validatorda baholash uchun validatsiyani umumiy ajdod kontrolda — `FormGroup`'da bajarishingiz kerak.
Qiymatlarini solishtirish uchun `FormGroup`'dan uning bola kontrollarini soʻraysiz.

`FormGroup`'ga validator qoʻshish uchun yaratish vaqtida yangi validatorni ikkinchi argument sifatida uzating.

```ts
const actorForm = new FormGroup(
  {
    'name': new FormControl(),
    'role': new FormControl(),
    'skill': new FormControl(),
  },
  {validators: unambiguousRoleValidator},
);
```

Validator kodi quyidagicha.

<docs-code header="unambiguous-role.directive.ts" path="adev/src/content/examples/form-validation/src/app/shared/unambiguous-role.directive.ts" region="cross-validation-validator"/>

`unambiguousRoleValidator` validatori `ValidatorFn` interfeysini amalga oshiradi.
U Angular kontrol obyektini argument sifatida qabul qiladi va forma toʻgʻri boʻlsa null, aks holda `ValidationErrors` qaytaradi.

Validator `FormGroup`'ning [get](api/forms/AbstractControl#get) metodini chaqirib bola kontrollarini oladi, keyin `name` va `role` kontrollarining qiymatlarini solishtiradi.

Agar qiymatlar mos kelmasa, rol bir maʼnoli, ikkalasi ham toʻgʻri va validator null qaytaradi.
Agar ular mos kelsa, aktyorning roli noaniq va validator xato obyektini qaytarib formani notoʻgʻri deb belgilashi kerak.

Yaxshiroq foydalanuvchi tajribasini taʼminlash uchun forma notoʻgʻri boʻlganda shablon tegishli xato xabarini koʻrsatadi.

<docs-code header="actor-form-reactive.component.html" path="adev/src/content/examples/form-validation/src/app/reactive/actor-form-reactive.component.html" region="cross-validation-error-message"/>

Bu `@if` `FormGroup`'da `unambiguousRoleValidator` validatori qaytargan maydonlararo validatsiya xatosi boʻlsa xatoni koʻrsatadi, lekin faqat foydalanuvchi [forma bilan oʻzaro aloqani](#control-status-css-classes) yakunlagan boʻlsa.

### Shablonga asoslangan formalarga maydonlararo validatsiya qoʻshish {#adding-cross-validation-to-template-driven-forms}

Shablonga asoslangan forma uchun validator funksiyasini oʻrab turuvchi direktiva yaratishingiz kerak.
Quyidagi misolda koʻrsatilganidek, bu direktivani [`NG_VALIDATORS` tokeni](/api/forms/NG_VALIDATORS) yordamida validator sifatida taqdim etasiz.

<docs-code header="unambiguous-role.directive.ts" path="adev/src/content/examples/form-validation/src/app/shared/unambiguous-role.directive.ts" region="cross-validation-directive"/>

Yangi direktivani HTML shabloniga qoʻshishingiz kerak.
Validator formaning eng yuqori darajasida roʻyxatdan oʻtkazilishi kerak boʻlgani sababli, quyidagi shablon direktivani `form` tegiga joylashtiradi.

<docs-code header="actor-form-template.component.html" path="adev/src/content/examples/form-validation/src/app/template/actor-form-template.component.html" region="cross-validation-register-validator"/>

Yaxshiroq foydalanuvchi tajribasini taʼminlash uchun forma notoʻgʻri boʻlganda tegishli xato xabari paydo boʻladi.

<docs-code header="actor-form-template.component.html" path="adev/src/content/examples/form-validation/src/app/template/actor-form-template.component.html" region="cross-validation-error-message"/>

Bu shablonga asoslangan formalarda ham, reaktiv formalarda ham bir xil.

## Asinxron validatorlar yaratish {#creating-asynchronous-validators}

Asinxron validatorlar `AsyncValidatorFn` va `AsyncValidator` interfeyslarini amalga oshiradi.
Ular oʻzlarining sinxron hamkasblariga juda oʻxshash, quyidagi farqlar bilan.

- `validate()` funksiyalari Promise yoki observable qaytarishi kerak,
- Qaytarilgan observable chekli boʻlishi kerak, yaʼni u qaysidir nuqtada yakunlanishi kerak.
  Cheksiz observable'ni cheklisiga aylantirish uchun observable'ni `first`, `last`, `take` yoki `takeUntil` kabi filtrlovchi operator orqali oʻtkazing.

Asinxron validatsiya sinxron validatsiyadan keyin sodir boʻladi va faqat sinxron validatsiya muvaffaqiyatli boʻlganda bajariladi.
Bu tekshiruv, agar oddiyroq validatsiya usullari allaqachon notoʻgʻri kiritmani aniqlagan boʻlsa, formalarga potensial qimmat asinxron validatsiya jarayonlaridan \(masalan, HTTP soʻrovi\) qochish imkonini beradi.

Asinxron validatsiya boshlangandan keyin forma kontroli `pending` holatiga kiradi.
Kontrolning `pending` xususiyatini tekshiring va davom etayotgan validatsiya operatsiyasi haqida vizual fikr-mulohaza berish uchun undan foydalaning.

Keng tarqalgan UI namunasi — asinxron validatsiya bajarilayotganda spinner koʻrsatish.
Quyidagi misol shablonga asoslangan formada bunga qanday erishishni koʻrsatadi.

```angular-html
<input [(ngModel)]="name" #model="ngModel" appSomeAsyncValidator />

@if (model.pending) {
  <app-spinner />
}
```

### Maxsus asinxron validatorni amalga oshirish {#implementing-a-custom-async-validator}

Quyidagi misolda asinxron validator aktyorlar hali band qilinmagan rolga tanlanishini taʼminlaydi.
Yangi aktyorlar doimo tanlovdan oʻtmoqda, eski aktyorlar esa nafaqaga chiqmoqda, shuning uchun mavjud rollar roʻyxatini oldindan olish mumkin emas.
Potensial rol kiritmasini validatsiya qilish uchun validator hozirda tanlangan barcha aktyorlarning markaziy maʼlumotlar bazasiga murojaat qiluvchi asinxron operatsiyani boshlashi kerak.

Quyidagi kod `AsyncValidator` interfeysini amalga oshiruvchi `UniqueRoleValidator` validator klassini yaratadi.

<docs-code header="role.directive.ts" path="adev/src/content/examples/form-validation/src/app/shared/role.directive.ts" region="async-validator"/>

`actorsService` xususiyati quyidagi interfeysni aniqlovchi `ActorsService` tokenining nusxasi bilan ishga tushiriladi.

```ts
interface ActorsService {
  isRoleTaken: (role: string) => Observable<boolean>;
}
```

Haqiqiy ilovada `ActorsService` rol mavjudligini tekshirish uchun aktyorlar maʼlumotlar bazasiga HTTP soʻrovi yuborish uchun masʼul boʻlar edi.
Validator nuqtai nazaridan servisning haqiqiy amalga oshirilishi muhim emas, shuning uchun misol shunchaki `ActorsService` interfeysiga tayanib kod yozishi mumkin.

Validatsiya boshlanganda `UniqueRoleValidator` joriy kontrol qiymati bilan `ActorsService`'ning `isRoleTaken()` metodiga vakolat beradi.
Bu nuqtada kontrol `pending` deb belgilanadi va `validate()` metodidan qaytarilgan observable zanjiri yakunlanmaguncha shu holatda qoladi.

`isRoleTaken()` metodi rol mavjudligini tekshiruvchi HTTP soʻrovini joʻnatadi va natija sifatida `Observable<boolean>` qaytaradi.
`validate()` metodi javobni `map` operatori orqali oʻtkazadi va uni validatsiya natijasiga aylantiradi.

Keyin metod, har qanday validator kabi, forma toʻgʻri boʻlsa `null`, aks holda `ValidationErrors` qaytaradi.
Bu validator har qanday potensial xatolarni `catchError` operatori bilan qayta ishlaydi.
Bu holda validator `isRoleTaken()` xatosini muvaffaqiyatli validatsiya sifatida koʻradi, chunki validatsiya soʻrovini yuborishdagi muvaffaqiyatsizlik rol notoʻgʻri ekanligini anglatmaydi.
Xatoni boshqacha qayta ishlab, oʻrniga `ValidationError` obyektini qaytarishingiz mumkin edi.

Biroz vaqt oʻtgach, observable zanjiri yakunlanadi va asinxron validatsiya tugaydi.
`pending` bayrogʻi `false` ga oʻrnatiladi va formaning validligi yangilanadi.

### Reaktiv formalarga asinxron validatorlarni qoʻshish {#adding-async-validators-to-reactive-forms}

Reaktiv formalarda asinxron validatordan foydalanish uchun validatorni komponent klassining xususiyatiga inyeksiya qilishdan boshlang.

<docs-code header="actor-form-reactive.component.ts" path="adev/src/content/examples/form-validation/src/app/reactive/actor-form-reactive.component.2.ts" region="async-validator-inject"/>

Keyin validator funksiyasini qoʻllash uchun uni toʻgʻridan-toʻgʻri `FormControl`'ga uzating.

Quyidagi misolda `UniqueRoleValidator`'ning `validate` funksiyasi `roleControl`'ga kontrolning `asyncValidators` opsiyasiga uzatish va uni `ActorFormReactiveComponent`'ga inyeksiya qilingan `UniqueRoleValidator` nusxasiga bogʻlash orqali qoʻllaniladi.
`asyncValidators` qiymati bitta asinxron validator funksiyasi yoki funksiyalar massivi boʻlishi mumkin.
`FormControl` opsiyalari haqida koʻproq bilish uchun [AbstractControlOptions](api/forms/AbstractControlOptions) API maʼlumotnomasiga qarang.

<docs-code header="actor-form-reactive.component.ts" path="adev/src/content/examples/form-validation/src/app/reactive/actor-form-reactive.component.2.ts" region="async-validator-usage"/>

### Shablonga asoslangan formalarga asinxron validatorlarni qoʻshish {#adding-async-validators-to-template-driven-forms}

Shablonga asoslangan formalarda asinxron validatordan foydalanish uchun yangi direktiva yarating va unda `NG_ASYNC_VALIDATORS` provider'ini roʻyxatdan oʻtkazing.

Quyidagi misolda direktiva haqiqiy validatsiya mantigʻini oʻz ichiga olgan `UniqueRoleValidator` klassini inyeksiya qiladi va uni validatsiya sodir boʻlishi kerak boʻlganda Angular tomonidan ishga tushiriladigan `validate` funksiyasida chaqiradi.

<docs-code header="role.directive.ts" path="adev/src/content/examples/form-validation/src/app/shared/role.directive.ts" region="async-validator-directive"/>

Keyin, sinxron validatorlardagi kabi, uni faollashtirish uchun direktivaning selektorini input'ga qoʻshing.

<docs-code header="actor-form-template.component.html (unique-unambiguous-role-input)" path="adev/src/content/examples/form-validation/src/app/template/actor-form-template.component.html" region="role-input"/>

### Asinxron validatorlarning samaradorligini optimallashtirish {#optimizing-performance-of-async-validators}

Sukut boʻyicha barcha validatorlar formaning har bir qiymat oʻzgarishidan keyin ishga tushadi.
Sinxron validatorlarda bu odatda ilova samaradorligiga sezilarli taʼsir koʻrsatmaydi.
Asinxron validatorlar esa kontrolni validatsiya qilish uchun odatda qandaydir HTTP soʻrovini bajaradi.
Har bir tugma bosilishidan keyin HTTP soʻrovini joʻnatish backend API'ga yuk boʻlishi mumkin va iloji boricha bundan qochish kerak.

`updateOn` xususiyatini `change` (sukut boʻyicha) qiymatidan `submit` yoki `blur` ga oʻzgartirish orqali forma validligini yangilashni kechiktirishingiz mumkin.

Shablonga asoslangan formalarda xususiyatni shablonda oʻrnating.

```angular-html
<input [(ngModel)]="name" [ngModelOptions]="{updateOn: 'blur'}" />
```

Reaktiv formalarda xususiyatni `FormControl` nusxasida oʻrnating.

```ts
new FormControl('', {updateOn: 'blur'});
```

## Reaktiv formalarda validatorlarni dinamik boshqarish {#managing-validators-dynamically-in-reactive-forms}

Murakkab reaktiv formalarda foydalanuvchi kiritmasi yoki ilova holatiga qarab validatorlarni qoʻshish, olib tashlash yoki oʻzgartirish kerak boʻlishi mumkin.
Angular forma kontrollarini qayta yaratmasdan validatorlarni ish vaqtida boshqarish uchun `AbstractControl`'da bir nechta metodlarni taqdim etadi.

### Validatorlarni qoʻshish va olib tashlash {#adding-and-removing-validators}

[`addValidators`](api/forms/AbstractControl#addValidators) va [`removeValidators`](api/forms/AbstractControl#removeValidators) metodlari kontrol validatorlarini ishga tushirilgandan keyin oʻzgartirish imkonini beradi.

```ts
onCountryChange(country: string) {
    const postalCodeControl = this.profileForm.get('postalCode');

    if (country === 'US') {
      // Add validators for US postal codes
      postalCodeControl.addValidators([Validators.required, Validators.pattern(/^\d{5}$/)]);
    } else {
      // Remove validators when not US
      postalCodeControl.removeValidators([Validators.required]);
    }

    postalCodeControl.updateValueAndValidity();
}
```

### Barcha validatorlarni almashtirish {#replacing-all-validators}

Kontroldagi barcha mavjud sinxron validatorlarni almashtirish uchun [`setValidators`](api/forms/AbstractControl#setValidators)'dan, barcha validatorlarni olib tashlash uchun esa [`clearValidators`](api/forms/AbstractControl#clearValidators)'dan foydalaning.

```ts
toggleStrictNameValidation(isStrict: boolean) {
  const nameControl = this.profileForm.get('name');

  if (isStrict) {
    // Set strict validation rules
    nameControl.setValidators([
      Validators.required,
      Validators.minLength(3),
      Validators.pattern(/^[a-zA-Z]+$/),
    ]);
  } else {
    // Clear all validators
    nameControl.clearValidators();
  }

  nameControl.updateValueAndValidity();
}
```

Xuddi shu namuna [`addAsyncValidators`](api/forms/AbstractControl#addAsyncValidators), [`removeAsyncValidators`](api/forms/AbstractControl#removeAsyncValidators), [`setAsyncValidators`](api/forms/AbstractControl#setAsyncValidators) va [`clearAsyncValidators`](api/forms/AbstractControl#clearAsyncValidators) yordamida asinxron validatorlarga ham qoʻllaniladi.

### Validatsiya yangilanishlarini ishga tushirish {#triggering-validation-updates}

Validatorlarni oʻzgartirgandan keyin kontrolning validatsiya holatini qayta hisoblash uchun [`updateValueAndValidity`](api/forms/AbstractControl#updateValueAndValidity)'ni chaqiring.
Bu metod yangilanish xatti-harakatini boshqarish uchun opsiyalarni qabul qiladi.

```ts
// Update control and notify parent
control.updateValueAndValidity();

// Update control only, don't notify parent or emit events
control.updateValueAndValidity({onlySelf: true, emitEvent: false});
```

## HTML'ning oʻz forma validatsiyasi bilan oʻzaro aloqa {#interaction-with-native-html-form-validation}

Sukut boʻyicha Angular oʻrab turuvchi `<form>`'ga `novalidate` atributini qoʻshish orqali [HTML'ning oʻz forma validatsiyasini](https://developer.mozilla.org/docs/Web/Guide/HTML/Constraint_validation) oʻchirib qoʻyadi va bu atributlarni freymvorkdagi validator funksiyalari bilan moslashtirish uchun direktivalardan foydalanadi.
Agar HTML'ning oʻz validatsiyasini Angular'ga asoslangan validatsiya **bilan birgalikda** ishlatmoqchi boʻlsangiz, uni `ngNativeValidate` direktivasi bilan qayta yoqishingiz mumkin.
Tafsilotlar uchun [API hujjatlariga](api/forms/NgForm#native-dom-validation-ui) qarang.
