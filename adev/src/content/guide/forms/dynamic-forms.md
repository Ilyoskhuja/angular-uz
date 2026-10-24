# Dinamik formalar yaratish

Soʻrovnomalar kabi koʻpgina formalar formati va maqsadi jihatidan bir-biriga juda oʻxshash boʻlishi mumkin.
Bunday formaning turli versiyalarini yaratishni tezroq va osonroq qilish uchun biznes obyekt modelini tavsiflovchi metadata asosida _dinamik forma shabloni_ yaratishingiz mumkin.
Keyin maʼlumotlar modelidagi oʻzgarishlarga mos ravishda yangi formalarni avtomatik yaratish uchun shu shablondan foydalanasiz.

Bu usul, ayniqsa, mazmuni tez oʻzgaruvchan biznes va tartibga solish talablariga javob berish uchun tez-tez oʻzgarishi kerak boʻlgan forma turiga ega boʻlganingizda foydali.
Odatiy foydalanish holati - soʻrovnoma.
Sizga turli kontekstlarda foydalanuvchilardan maʼlumot olish kerak boʻlishi mumkin.
Foydalanuvchi koʻradigan formalarning formati va uslubi oʻzgarmas qolishi kerak, soʻralishi kerak boʻlgan haqiqiy savollar esa kontekstga qarab oʻzgaradi.

Bu darslikda siz oddiy soʻrovnomani taqdim etuvchi dinamik forma yaratasiz.
Siz ish izlayotgan qahramonlar uchun onlayn ariza ilovasini yaratasiz.
Agentlik ariza berish jarayonini doimiy oʻzgartirib turadi, lekin dinamik formadan foydalanib,
ilova kodini oʻzgartirmasdan yangi formalarni ish jarayonida yaratishingiz mumkin.

Darslik sizni quyidagi qadamlar boʻylab olib oʻtadi:

1. Loyiha uchun reaktiv formalarni yoqish.
1. Forma kontrollarini ifodalash uchun maʼlumotlar modelini yaratish.
1. Modelni namunaviy maʼlumotlar bilan toʻldirish.
1. Forma kontrollarini dinamik yaratuvchi komponent ishlab chiqish.

Siz yaratadigan forma foydalanuvchi tajribasini yaxshilash uchun kiritilgan maʼlumotlar validatsiyasi va stillardan foydalanadi.
Unda faqat barcha foydalanuvchi kiritmalari valid boʻlganda yoqiladigan Yuborish (Submit) tugmasi bor va u notoʻgʻri kiritmalarni rang kodlari va xato xabarlari bilan belgilaydi.

Oddiy versiya savollarning boyroq turlarini, chiroyliroq render qilishni va yuqoriroq foydalanuvchi tajribasini qoʻllab-quvvatlash uchun rivojlanishi mumkin.

## Loyihangiz uchun reaktiv formalarni yoqish {#enable-reactive-forms-for-your-project}

Dinamik formalar reaktiv formalarga asoslanadi.

Ilovaga reaktiv forma direktivalariga kirish imkonini berish uchun `@angular/forms` paketidan `ReactiveFormsModule`'ni kerakli komponentlarga import qiling.

<docs-code-multifile>
    <docs-code header="dynamic-form.component.ts" path="adev/src/content/examples/dynamic-form/src/app/dynamic-form.component.ts"/>
    <docs-code header="dynamic-form-question.component.ts" path="adev/src/content/examples/dynamic-form/src/app/dynamic-form-question.component.ts"/>
</docs-code-multifile>

## Forma obyekt modelini yaratish {#create-a-form-object-model}

Dinamik forma uchun forma funksionalligiga kerak boʻlgan barcha stsenariylarni tavsiflay oladigan obyekt modeli talab qilinadi.
Misoldagi qahramon-ariza formasi savollar toʻplamidir — yaʼni formadagi har bir kontrol savol berishi va javob qabul qilishi kerak.

Bunday forma turi uchun maʼlumotlar modeli savolni ifodalashi kerak.
Misolda savolni modeldagi asosiy obyekt sifatida belgilaydigan `DynamicFormQuestionComponent` mavjud.

Quyidagi `QuestionBase` formada savol va uning javobini ifodalay oladigan kontrollar toʻplami uchun asos (base) klassdir.

<docs-code header="question-base.ts" path="adev/src/content/examples/dynamic-form/src/app/question-base.ts"/>

### Kontrol klasslarini belgilash {#define-control-classes}

Misol shu asosdan turli kontrol turlarini ifodalovchi ikkita yangi klass — `TextboxQuestion` va `DropdownQuestion` — hosil qiladi.
Keyingi qadamda forma shablonini yaratganingizda, tegishli kontrollarni dinamik render qilish uchun shu muayyan savol turlaridan nusxa (instance) yaratasiz.

`TextboxQuestion` kontrol turi forma shablonida `<input>` elementi yordamida ifodalanadi. U savolni taqdim etadi va foydalanuvchilarga maʼlumot kiritish imkonini beradi. Elementning `type` atributi `options` argumentida koʻrsatilgan `type` maydoni asosida belgilanadi (masalan, `text`, `email`, `url`).

<docs-code header="question-textbox.ts" path="adev/src/content/examples/dynamic-form/src/app/question-textbox.ts"/>

`DropdownQuestion` kontrol turi tanlov roʻyxatida (select box) variantlar roʻyxatini taqdim etadi.

 <docs-code header="question-dropdown.ts" path="adev/src/content/examples/dynamic-form/src/app/question-dropdown.ts"/>

### Forma guruhlarini tuzish {#compose-form-groups}

Dinamik forma forma modeli asosida guruhlangan input kontrollar toʻplamlarini yaratish uchun servisdan foydalanadi.
Quyidagi `QuestionControlService` savol modelidagi metadatadan foydalanuvchi `FormGroup` nusxalari toʻplamini yigʻadi.
Siz sukut boʻyicha qiymatlar va validatsiya qoidalarini koʻrsatishingiz mumkin.

<docs-code header="question-control.service.ts" path="adev/src/content/examples/dynamic-form/src/app/question-control.service.ts"/>

## Dinamik forma mazmunini tuzish {#compose-dynamic-form-contents}

Dinamik formaning oʻzi keyingi qadamda qoʻshadigan konteyner komponent orqali ifodalanadi.
Har bir savol forma komponenti shablonida `DynamicFormQuestionComponent` nusxasiga mos keluvchi `<app-question>` tegi orqali ifodalanadi.

`DynamicFormQuestionComponent` maʼlumotlarga bogʻlangan savol obyektidagi qiymatlar asosida alohida savolning tafsilotlarini render qilish uchun javobgar.
Forma shablon HTML'ini asosiy kontrol obyektlariga ulash uchun [`[formGroup]` direktivasiga](api/forms/FormGroupDirective 'API maʼlumotnomasi') tayanadi.
`DynamicFormQuestionComponent` forma guruhlarini yaratadi va ularni savol modelida belgilangan kontrollar bilan toʻldiradi, koʻrsatish va validatsiya qoidalarini belgilaydi.

<docs-code-multifile>
  <docs-code header="dynamic-form-question.component.html" path="adev/src/content/examples/dynamic-form/src/app/dynamic-form-question.component.html"/>
  <docs-code header="dynamic-form-question.component.ts" path="adev/src/content/examples/dynamic-form/src/app/dynamic-form-question.component.ts"/>
</docs-code-multifile>

`DynamicFormQuestionComponent`'ning maqsadi modelingizda belgilangan savol turlarini taqdim etishdir.
Hozircha sizda faqat ikki turdagi savol bor, lekin yana koʻplab turlarni tasavvur qilishingiz mumkin.
Shablondagi `@switch` bloki qaysi turdagi savolni koʻrsatishni aniqlaydi.
Switch [`formControlName`](api/forms/FormControlName 'FormControlName direktivasi API maʼlumotnomasi') va [`formGroup`](api/forms/FormGroupDirective 'FormGroupDirective API maʼlumotnomasi') selektorlariga ega direktivalardan foydalanadi.
Ikkala direktiva ham `ReactiveFormsModule`'da belgilangan.

### Maʼlumotlarni taqdim etish {#supply-data}

Alohida formani yaratish uchun muayyan savollar toʻplamini taqdim etuvchi boshqa servis kerak.
Bu mashq uchun siz qattiq kodlangan namunaviy maʼlumotlardan ushbu savollar massivini taqdim etuvchi `QuestionService`'ni yaratasiz.
Haqiqiy ilovada servis maʼlumotlarni backend tizimidan olishi mumkin.
Biroq asosiy jihat shundaki, qahramonlarning ishga ariza savollarini toʻliq `QuestionService` qaytargan obyektlar orqali boshqarasiz.
Talablar oʻzgarganda soʻrovnomani yuritish uchun faqat `questions` massividagi obyektlarni qoʻshish, yangilash va olib tashlash kifoya.

`QuestionService` savollar toʻplamini `input()` savollariga bogʻlangan massiv koʻrinishida taqdim etadi.

<docs-code header="question.service.ts" path="adev/src/content/examples/dynamic-form/src/app/question.service.ts"/>

## Dinamik forma shablonini yaratish {#create-a-dynamic-form-template}

`DynamicFormComponent` komponenti forma uchun kirish nuqtasi va asosiy konteyner boʻlib, shablonda `<app-dynamic-form>` yordamida ifodalanadi.

`DynamicFormComponent` komponenti har bir savolni `DynamicFormQuestionComponent`'ga mos keluvchi `<app-question>` elementiga bogʻlab, savollar roʻyxatini taqdim etadi.

<docs-code-multifile>
    <docs-code header="dynamic-form.component.html" path="adev/src/content/examples/dynamic-form/src/app/dynamic-form.component.html"/>
    <docs-code header="dynamic-form.component.ts" path="adev/src/content/examples/dynamic-form/src/app/dynamic-form.component.ts"/>
</docs-code-multifile>

### Formani koʻrsatish {#display-the-form}

Dinamik forma nusxasini koʻrsatish uchun `AppComponent` qobiq shabloni `QuestionService` qaytargan `questions` massivini forma konteyner komponenti `<app-dynamic-form>`'ga uzatadi.

<docs-code header="app.component.ts" path="adev/src/content/examples/dynamic-form/src/app/app.component.ts"/>

Model va maʼlumotlarning bunday ajratilishi komponentlarni _savol_ obyekt modeliga mos boʻlgan istalgan turdagi soʻrovnoma uchun qayta ishlatish imkonini beradi.

### Maʼlumotlar validligini taʼminlash {#ensuring-valid-data}

Forma shabloni muayyan savollar haqida qattiq kodlangan hech qanday taxminlar qilmasdan formani render qilish uchun metadataning dinamik bogʻlanishidan foydalanadi.
U kontrol metadatasini ham, validatsiya mezonlarini ham dinamik qoʻshadi.

Kiritilgan maʼlumotlar validligini taʼminlash uchun _Save_ tugmasi forma valid holatga kelgunga qadar oʻchirilgan boʻladi.
Forma valid boʻlganda _Save_ tugmasini bosing va ilova joriy forma qiymatlarini JSON koʻrinishida render qiladi.

Quyidagi rasmda yakuniy forma koʻrsatilgan.

<img alt="Dynamic-Form" src="assets/images/guide/dynamic-form/dynamic-form.png">

## Keyingi qadamlar {#next-steps}

<docs-pill-row>
  <docs-pill title="Forma kiritmalarini validatsiya qilish" href="guide/forms/reactive-forms#validating-form-input" />
  <docs-pill title="Forma validatsiyasi qoʻllanmasi" href="guide/forms/form-validation" />
</docs-pill-row>
