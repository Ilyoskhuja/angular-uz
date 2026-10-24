# Shablonga asoslangan forma yaratish

Bu darslik sizga shablonga asoslangan forma (template-driven form) yaratishni koʻrsatadi. Formadagi boshqaruv elementlari (controls) kiritish validatsiyasiga ega maʼlumot xususiyatlariga bogʻlanadi. Kiritish validatsiyasi maʼlumotlar yaxlitligini saqlashga va foydalanuvchi tajribasini yaxshilash uchun stillar berishga yordam beradi.

Shablonga asoslangan formalar shablonda oʻzgarishlar kiritilganda komponentdagi maʼlumotlar modelini yangilash uchun (va aksincha) [ikki tomonlama maʼlumot bogʻlash](guide/templates/two-way-binding)dan foydalanadi.

<docs-callout helpful title="Shablonga asoslangan va reaktiv formalar">
Angular interaktiv formalar uchun ikkita dizayn yondashuvini qoʻllab-quvvatlaydi. Shablonga asoslangan formalar Angular shabloningizda formaga xos direktivalardan foydalanish imkonini beradi. Reaktiv formalar formalar yaratishga modelga asoslangan yondashuvni taqdim etadi.

Shablonga asoslangan formalar kichik yoki sodda formalar uchun ajoyib tanlov, reaktiv formalar esa yaxshiroq masshtablanadi va murakkab formalar uchun mos keladi. Ikki yondashuvni solishtirish uchun [Yondashuvni tanlash](guide/forms#choosing-an-approach) boʻlimiga qarang
</docs-callout>

Angular shabloni bilan deyarli har qanday turdagi formani yaratishingiz mumkin — kirish formalari, aloqa formalari va amalda istalgan biznes formasi.
Boshqaruv elementlarini ijodiy joylashtirishingiz va ularni obyekt modelingizdagi maʼlumotlarga bogʻlashingiz mumkin.
Validatsiya qoidalarini belgilashingiz va validatsiya xatolarini koʻrsatishingiz, muayyan boshqaruv elementlaridan kiritishga shartli ruxsat berishingiz, oʻrnatilgan vizual qayta aloqani ishga tushirishingiz va yana koʻp narsalarni qilishingiz mumkin.

## Maqsadlar {#objectives}

Bu darslik sizga quyidagilarni oʻrgatadi:

- Komponent va shablon bilan Angular formasini yaratish
- Input boshqaruv elementlari qiymatlarini oʻqish va yozish uchun `ngModel` yordamida ikki tomonlama maʼlumot bogʻlashlarini yaratish
- Boshqaruv elementlari holatini kuzatuvchi maxsus CSS klasslari yordamida vizual qayta aloqa berish
- Foydalanuvchilarga validatsiya xatolarini koʻrsatish va forma holatiga qarab forma boshqaruv elementlaridan kiritishga shartli ruxsat berish
- [Shablon murojaat oʻzgaruvchilari](guide/templates/variables#template-reference-variables) yordamida HTML elementlari oʻrtasida maʼlumot ulashish

## Shablonga asoslangan forma yaratish {#build-a-template-driven-form}

Shablonga asoslangan formalar `FormsModule`'da aniqlangan direktivalarga tayanadi.

| Direktivalar   | Tafsilotlar                                                                                                                                                                                                                                                                      |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `NgModel`      | Biriktirilgan forma elementidagi qiymat oʻzgarishlarini maʼlumotlar modelidagi oʻzgarishlar bilan moslashtiradi va foydalanuvchi kiritishiga kiritish validatsiyasi va xatolarga ishlov berish bilan javob qaytarish imkonini beradi.                                            |
| `NgForm`       | Yuqori darajali `FormGroup` nusxasini yaratadi va formaning umumiy qiymati hamda validatsiya holatini kuzatish uchun uni `<form>` elementiga bogʻlaydi. `FormsModule`'ni import qilishingiz bilan bu direktiva sukut boʻyicha barcha `<form>` teglarida faol boʻladi. Maxsus selektor qoʻshish shart emas. |
| `NgModelGroup` | `FormGroup` nusxasini yaratadi va uni DOM elementiga bogʻlaydi.                                                                                                                                                                                                                 |

### Qadamlar umumiy koʻrinishi {#step-overview}

Bu darslik davomida siz namunaviy formani maʼlumotlarga bogʻlaysiz va quyidagi qadamlar yordamida foydalanuvchi kiritishiga ishlov berasiz.

1. Asosiy formani yarating.
   - Namunaviy maʼlumotlar modelini aniqlang
   - `FormsModule` kabi zarur infratuzilmani qoʻshing
1. `ngModel` direktivi va ikki tomonlama maʼlumot bogʻlash sintaksisi yordamida forma boshqaruv elementlarini maʼlumot xususiyatlariga bogʻlang.
   - `ngModel` boshqaruv elementlari holatlarini CSS klasslari orqali qanday bildirishini koʻrib chiqing
   - Boshqaruv elementlariga `ngModel` uchun mavjud boʻlishi maqsadida nom bering
1. `ngModel` yordamida kiritish validligini va boshqaruv elementi holatini kuzating.
   - Holat haqida vizual qayta aloqa berish uchun maxsus CSS qoʻshing
   - Validatsiya xatosi xabarlarini koʻrsating va yashiring
1. Model maʼlumotlariga qoʻshish orqali HTML tugmasining native bosish hodisasiga javob bering.
1. Formaning [`ngSubmit`](api/forms/NgForm#ngSubmit) output xususiyati yordamida forma yuborilishiga ishlov bering.
   - Forma valid boʻlmaguncha **Submit** tugmasini oʻchirib qoʻying
   - Yuborilgandan soʻng tugallangan formani sahifadagi boshqa kontent bilan almashtiring

## Formani yaratish {#build-the-form}

<!-- TODO: link to preview -->
<!-- <docs-code live/> -->

1. Taqdim etilgan namunaviy ilova formada aks etadigan maʼlumotlar modelini aniqlovchi `Actor` klassini yaratadi.

   <docs-code header="actor.ts" language="typescript" path="adev/src/content/examples/forms/src/app/actor.ts"/>

1. Forma joylashuvi va tafsilotlari `ActorFormComponent` klassida aniqlanadi.

   <docs-code header="actor-form.component.ts (v1)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.ts" region="v1"/>

   Komponentning `selector` qiymati "app-actor-form" boʻlgani uchun bu formani `<app-actor-form>` tegi yordamida ota shablonga joylashtirishingiz mumkin.

1. Quyidagi kod yangi aktyor nusxasini yaratadi, shunda dastlabki forma namunaviy aktyorni koʻrsata oladi.

   <docs-code language="typescript" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.ts" language="typescript" region="Marilyn"/>

   Bu demo `model` va `skills` uchun soxta maʼlumotlardan foydalanadi.
   Haqiqiy ilovada haqiqiy maʼlumotlarni olish va saqlash uchun maʼlumotlar servisini inyeksiya qilgan yoki bu xususiyatlarni input va output sifatida ochib bergan boʻlardingiz.

1. Komponent `FormsModule` modulini import qilish orqali Forms imkoniyatini yoqadi.

   <docs-code language="typescript" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.ts" language="typescript" region="imports"/>

1. Forma ildiz komponent shablonida aniqlangan ilova joylashuvida koʻrsatiladi.

   <docs-code header="app.component.html" language="html" path="adev/src/content/examples/forms/src/app/app.component.html"/>

   Dastlabki shablon ikkita forma guruhi va yuborish tugmasiga ega forma joylashuvini aniqlaydi.
   Forma guruhlari Actor maʼlumotlar modelining ikkita xususiyatiga — name va studio — mos keladi.
   Har bir guruhda yorliq (label) va foydalanuvchi kiritishi uchun katakcha bor.
   - **Name** `<input>` boshqaruv elementida HTML5 `required` atributi bor
   - **Studio** `<input>` boshqaruv elementida esa yoʻq, chunki `studio` ixtiyoriy

   **Submit** tugmasida stillar berish uchun bir nechta klass bor.
   Hozircha forma joylashuvi hech qanday bogʻlash yoki direktivalarsiz, butunlay oddiy HTML5'dan iborat.

1. Namunaviy forma [Twitter Bootstrap](https://getbootstrap.com/css)'dan bir nechta stil klasslaridan foydalanadi: `container`, `form-group`, `form-control` va `btn`.
   Bu stillardan foydalanish uchun ilovaning stil fayli kutubxonani import qiladi.

   <docs-code header="styles.css" path="adev/src/content/examples/forms/src/styles.1.css"/>

1. Forma aktyor mahorati (skill) `ActorFormComponent` ichida saqlanadigan oldindan belgilangan `skills` roʻyxatidan tanlanishini talab qiladi.
   Angular `@for` sikli `<select>` elementini toʻldirish uchun maʼlumot qiymatlari boʻylab takrorlanadi.

   <docs-code header="actor-form.component.html (skills)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="skills"/>

Agar ilovani hozir ishga tushirsangiz, tanlov boshqaruv elementida mahoratlar roʻyxatini koʻrasiz.
Input elementlari hali maʼlumot qiymatlariga yoki hodisalarga bogʻlanmagan, shuning uchun ular hali boʻsh va hech qanday xatti-harakatga ega emas.

## Input boshqaruv elementlarini maʼlumot xususiyatlariga bogʻlash {#bind-input-controls-to-data-properties}

Keyingi qadam — input boshqaruv elementlarini tegishli `Actor` xususiyatlariga ikki tomonlama maʼlumot bogʻlash orqali bogʻlash, shunda ular foydalanuvchi kiritishiga maʼlumotlar modelini yangilash bilan, maʼlumotlardagi dasturiy oʻzgarishlarga esa koʻrinishni yangilash bilan javob beradi.

`FormsModule`'da eʼlon qilingan `ngModel` direktivi shablonga asoslangan formangizdagi boshqaruv elementlarini maʼlumotlar modelingizdagi xususiyatlarga bogʻlash imkonini beradi.
Direktivani ikki tomonlama maʼlumot bogʻlash sintaksisi `[(ngModel)]` bilan qoʻshganingizda, Angular boshqaruv elementining qiymatini va foydalanuvchi bilan oʻzaro aloqasini kuzatib, koʻrinishni model bilan sinxron saqlay oladi.

1. `actor-form.component.html` shablon faylini tahrirlang.
1. **Name** yorligʻi yonidagi `<input>` tegini toping.
1. Ikki tomonlama maʼlumot bogʻlash sintaksisi `[(ngModel)]="..."` yordamida `ngModel` direktivini qoʻshing.

<docs-code header="actor-form.component.html (excerpt)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="ngModelName-1"/>

HELPFUL: Bu misolda har bir input tegidan keyin tegishli xususiyatning joriy maʼlumot qiymatini koʻrsatish uchun vaqtinchalik diagnostik interpolyatsiya `{{model.name}}` bor. Izoh ikki tomonlama maʼlumot bogʻlashning ishlashini kuzatib boʻlganingizdan soʻng diagnostik qatorlarni olib tashlashni eslatadi.

### Formaning umumiy holatiga murojaat qilish {#access-the-overall-form-status}

Komponentingizga `FormsModule`'ni import qilganingizda, Angular shablondagi `<form>` tegiga avtomatik ravishda [NgForm](api/forms/NgForm) direktivasini yaratib biriktirdi (chunki `NgForm` `<form>` elementlariga mos keladigan `form` selektoriga ega).

`NgForm`'ga va formaning umumiy holatiga murojaat qilish uchun [shablon murojaat oʻzgaruvchisi](guide/templates/variables#template-reference-variables)ni eʼlon qiling.

1. `actor-form.component.html` shablon faylini tahrirlang.
1. `<form>` tegini `#actorForm` shablon murojaat oʻzgaruvchisi bilan yangilang va uning qiymatini quyidagicha oʻrnating.

   <docs-code header="actor-form.component.html (excerpt)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="template-variable"/>

   `actorForm` shablon oʻzgaruvchisi endi formani yaxlit boshqaradigan `NgForm` direktivasi nusxasiga murojaatdir.

1. Ilovani ishga tushiring.
1. **Name** input katakchasiga yozishni boshlang.

   Belgilarni qoʻshganingizda va oʻchirganingizda ular maʼlumotlar modelida paydo boʻlishini va yoʻqolishini koʻrishingiz mumkin.

Interpolyatsiya qilingan qiymatlarni koʻrsatuvchi diagnostik qator qiymatlar haqiqatan ham input katakchasidan modelga va yana qaytib oqayotganini namoyish etadi.

### Boshqaruv elementlariga nom berish {#naming-control-elements}

Elementda `[(ngModel)]`'dan foydalanganingizda, oʻsha element uchun `name` atributini aniqlashingiz shart.
Angular berilgan nomdan elementni ota `<form>` elementiga biriktirilgan `NgForm` direktivasida roʻyxatdan oʻtkazish uchun foydalanadi.

Misolda `<input>` elementiga `name` atributi qoʻshilib, "name" qiymatiga oʻrnatildi — bu aktyor ismi uchun mantiqan toʻgʻri.
Har qanday noyob qiymat yetarli, lekin tavsiflovchi nom ishlatish foydali.

1. **Studio** va **Skill**'ga ham shunga oʻxshash `[(ngModel)]` bogʻlashlari va `name` atributlarini qoʻshing.
1. Endi interpolyatsiya qilingan qiymatlarni koʻrsatuvchi diagnostik xabarlarni olib tashlashingiz mumkin.
1. Ikki tomonlama maʼlumot bogʻlash butun aktyor modeli uchun ishlashini tasdiqlash uchun komponent shablonining yuqori qismiga maʼlumotlarni satrga seriyalashtiruvchi [`json`](api/common/JsonPipe) pipe bilan yangi matn bogʻlashini qoʻshing.

Bu oʻzgarishlardan soʻng forma shabloni quyidagicha koʻrinishi kerak:

<docs-code header="actor-form.component.html (excerpt)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="ngModel-2"/>

Eʼtibor bering:

- Har bir `<input>` elementida `id` xususiyati bor.
  U `<label>` elementining `for` atributi tomonidan yorliqni oʻz input boshqaruv elementiga moslashtirish uchun ishlatiladi.
  Bu [standart HTML imkoniyati](https://developer.mozilla.org/docs/Web/HTML/Element/label).

- Har bir `<input>` elementida shuningdek Angular boshqaruv elementini formada roʻyxatdan oʻtkazish uchun ishlatadigan zarur `name` xususiyati ham bor.

Natijalarni kuzatib boʻlganingizdan soʻng `{{ model | json }}` matn bogʻlashini oʻchirib tashlashingiz mumkin.

## Forma holatlarini kuzatish {#track-form-states}

Angular forma yuborilgandan soʻng `form` elementlariga `ng-submitted` klassini qoʻllaydi. Bu klassdan forma yuborilgandan keyin uning stilini oʻzgartirish uchun foydalanish mumkin.

## Boshqaruv elementlari holatlarini kuzatish {#track-control-states}

Boshqaruv elementiga `NgModel` direktivasini qoʻshish unga holatini tavsiflovchi klass nomlarini qoʻshadi.
Bu klasslardan boshqaruv elementining stilini uning holatiga qarab oʻzgartirish uchun foydalanish mumkin.

Quyidagi jadval Angular boshqaruv elementi holatiga qarab qoʻllaydigan klass nomlarini tavsiflaydi.

| Holatlar                                         | Rost boʻlsa klass | Yolgʻon boʻlsa klass |
| :----------------------------------------------- | :---------------- | :------------------- |
| Boshqaruv elementiga kirilgan.                   | `ng-touched`      | `ng-untouched`       |
| Boshqaruv elementining qiymati oʻzgargan.        | `ng-dirty`        | `ng-pristine`        |
| Boshqaruv elementining qiymati valid.            | `ng-valid`        | `ng-invalid`         |

Angular shuningdek yuborilganda `form` elementlariga `ng-submitted` klassini ham qoʻllaydi, lekin `form` elementi ichidagi boshqaruv elementlariga qoʻllamaydi.

Bu CSS klasslaridan boshqaruv elementingiz uchun holatiga qarab stillarni aniqlashda foydalanasiz.

### Boshqaruv elementlari holatlarini kuzatib koʻrish {#observe-control-states}

Freymvork klasslarni qanday qoʻshishi va olib tashlashini koʻrish uchun brauzerning dasturchi vositalarini oching va aktyor ismini ifodalovchi `<input>` elementini tekshiring.

1. Brauzeringizning dasturchi vositalari yordamida **Name** input katakchasiga mos keladigan `<input>` elementini toping.
   Elementda "form-control"dan tashqari bir nechta CSS klasslari borligini koʻrishingiz mumkin.

1. Uni birinchi marta ochganingizda klasslar u valid qiymatga ega ekanini, qiymat initsializatsiya yoki qayta oʻrnatishdan beri oʻzgarmaganini va boshqaruv elementiga initsializatsiya yoki qayta oʻrnatishdan beri kirilmaganini bildiradi.

   ```html
   <input class="form-control ng-untouched ng-pristine ng-valid" />
   ```

1. **Name** `<input>` katakchasida quyidagi amallarni bajaring va qaysi klasslar paydo boʻlishini kuzating.
   - Qarang, lekin tegmang.
     Klasslar u tegilmagan (untouched), oʻzgarmagan (pristine) va valid ekanini bildiradi.

   - Ism katakchasi ichiga bosing, keyin uning tashqarisiga bosing.
     Boshqaruv elementiga endi kirilgan va elementda `ng-untouched` klassi oʻrniga `ng-touched` klassi bor.

   - Ism oxiriga slesh belgilarini qoʻshing.
     Endi u tegilgan (touched) va oʻzgargan (dirty).

   - Ismni oʻchiring.
     Bu qiymatni invalid qiladi, shuning uchun `ng-valid` klassi oʻrnini `ng-invalid` klassi egallaydi.

### Holatlar uchun vizual qayta aloqa yaratish {#create-visual-feedback-for-states}

`ng-valid`/`ng-invalid` juftligi ayniqsa qiziq, chunki qiymatlar invalid boʻlganda
kuchli vizual signal berishni istaysiz.
Shuningdek, majburiy maydonlarni ham belgilashni istaysiz.

Majburiy maydonlarni va invalid maʼlumotlarni input katakchasining chap tomonidagi rangli
chiziq bilan bir vaqtning oʻzida belgilashingiz mumkin.

Koʻrinishni shu tarzda oʻzgartirish uchun quyidagi qadamlarni bajaring.

1. `ng-*` CSS klasslari uchun taʼriflar qoʻshing.
1. Bu klass taʼriflarini yangi `forms.css` fayliga qoʻshing.
1. Yangi faylni loyihaga `index.html` bilan bir qatorda joylashtiring:

   <docs-code header="forms.css" language="css" path="adev/src/content/examples/forms/src/assets/forms.css"/>

1. `index.html` faylida `<head>` tegini yangi stil faylini qoʻshadigan tarzda yangilang.

   <docs-code header="index.html (styles)" path="adev/src/content/examples/forms/src/index.html" region="styles"/>

### Validatsiya xatosi xabarlarini koʻrsatish va yashirish {#show-and-hide-validation-error-messages}

**Name** input katakchasi majburiy va uni tozalash chiziqni qizil rangga oʻzgartiradi.
Bu nimadir notoʻgʻri ekanini bildiradi, lekin foydalanuvchi nima notoʻgʻri yoki nima qilish kerakligini bilmaydi.
Boshqaruv elementi holatini tekshirib, unga javob berish orqali foydali xabar taqdim etishingiz mumkin.

**Skill** tanlov katakchasi ham majburiy, lekin unga bunday xatolarga ishlov berish kerak emas, chunki tanlov katakchasi tanlovni allaqachon valid qiymatlar bilan cheklaydi.

Kerak boʻlganda xato xabarini aniqlash va koʻrsatish uchun quyidagi qadamlarni bajaring.

<docs-workflow>
<docs-step title="Input'ga lokal murojaat qoʻshing">
`input` tegini shablon ichidan input katakchasining Angular boshqaruv elementiga murojaat qilish uchun ishlatishingiz mumkin boʻlgan shablon murojaat oʻzgaruvchisi bilan kengaytiring. Misolda oʻzgaruvchi `#name="ngModel"`.

Shablon murojaat oʻzgaruvchisi (`#name`) `"ngModel"` qiymatiga oʻrnatiladi, chunki bu [`NgModel.exportAs`](api/core/Directive#exportAs) xususiyatining qiymati. Bu xususiyat Angular'ga murojaat oʻzgaruvchisini direktivaga qanday bogʻlashni aytadi.
</docs-step>

<docs-step title="Xato xabarini qoʻshing">
Mos xato xabarini oʻz ichiga olgan `<div>` qoʻshing.
</docs-step>

<docs-step title="Xato xabarini shartli qiling">
`name` boshqaruv elementining xususiyatlarini xabar `<div>` elementining `hidden` xususiyatiga bogʻlash orqali xato xabarini koʻrsating yoki yashiring.
</docs-step>

<docs-code header="actor-form.component.html (hidden-error-msg)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="hidden-error-msg"/>

<docs-step title="name'ga shartli xato xabarini qoʻshing">
Quyidagi misoldagidek, `name` input katakchasiga shartli xato xabarini qoʻshing.

<docs-code header="actor-form.component.html (excerpt)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="name-with-error-msg"/>
</docs-step>
</docs-workflow>

<docs-callout title='"Pristine" holatini tushuntirish'>

Bu misolda boshqaruv elementi valid yoki _pristine_ (oʻzgarmagan) boʻlganda xabarni yashirasiz.
Pristine foydalanuvchi qiymatni bu formada koʻrsatilganidan beri oʻzgartirmaganini anglatadi.
Agar `pristine` holatini eʼtiborsiz qoldirsangiz, xabarni faqat qiymat valid boʻlganda yashirgan boʻlardingiz.
Agar bu komponentga yangi, boʻsh aktyor yoki invalid aktyor bilan kirsangiz, hech narsa qilmasingizdan oldin xato xabarini darhol koʻrasiz.

Xabar faqat foydalanuvchi invalid oʻzgarish kiritganda koʻrsatilishini istashingiz mumkin.
Boshqaruv elementi `pristine` holatida boʻlganida xabarni yashirish shu maqsadga erishadi.
Keyingi qadamda formaga yangi aktyor qoʻshganingizda bu tanlovning ahamiyatini koʻrasiz.

</docs-callout>

## Yangi aktyor qoʻshish {#add-a-new-actor}

Bu mashq model maʼlumotlariga qoʻshish orqali HTML tugmasining native bosish hodisasiga qanday javob berishingiz mumkinligini koʻrsatadi.
Forma foydalanuvchilariga yangi aktyor qoʻshish imkonini berish uchun bosish hodisasiga javob beradigan **New Actor** tugmasini qoʻshasiz.

1. Shablonda formaning pastki qismiga "New Actor" `<button>` elementini joylashtiring.
1. Komponent faylida aktyor maʼlumotlar modeliga aktyor yaratish metodini qoʻshing.

   <docs-code header="actor-form.component.ts (New Actor method)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.ts" region="new-actor"/>

1. Tugmaning bosish hodisasini aktyor yaratish metodi `newActor()`'ga bogʻlang.

   <docs-code header="actor-form.component.html (New Actor button)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="new-actor-button-no-reset"/>

1. Ilovani qayta ishga tushiring va **New Actor** tugmasini bosing.

   Forma tozalanadi va input katakchasining chap tomonidagi _majburiy_ chiziqlar qizil boʻlib, `name` va `skill` xususiyatlari invalid ekanini bildiradi.
   Xato xabarlari yashirilganiga eʼtibor bering.
   Buning sababi forma pristine holatda; siz hali hech narsani oʻzgartirmadingiz.

1. Ism kiriting va yana **New Actor** tugmasini bosing.

   Endi ilova `Name is required` xato xabarini koʻrsatadi, chunki input katakchasi endi pristine emas.
   Forma **New Actor** tugmasini bosishdan oldin ism kiritganingizni eslab qoladi.

1. Forma boshqaruv elementlarining pristine holatini tiklash uchun `newActor()` metodini chaqirgandan soʻng formaning `reset()` metodini chaqirib, barcha bayroqlarni imperativ tarzda tozalang.

   <docs-code header="actor-form.component.html (Reset the form)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="new-actor-button-form-reset"/>

   Endi **New Actor** tugmasini bosish formani ham, uning boshqaruv elementlari bayroqlarini ham qayta oʻrnatadi.

## Formani `ngSubmit` bilan yuborish {#submit-the-form-with-ngsubmit}

Foydalanuvchi bu formani toʻldirgandan soʻng yubora olishi kerak.
Formaning pastki qismidagi **Submit** tugmasi oʻz-oʻzidan hech narsa qilmaydi, lekin turi (`type="submit"`) tufayli forma yuborish hodisasini ishga tushiradi.

Bu hodisaga javob berish uchun quyidagi qadamlarni bajaring.

<docs-workflow>

<docs-step title="ngOnSubmit'ni tinglang">
Formaning [`ngSubmit`](api/forms/NgForm#ngSubmit) hodisa xususiyatini aktyor formasi komponentining `onSubmit()` metodiga bogʻlang.

<docs-code header="actor-form.component.html (ngSubmit)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="ngSubmit"/>
</docs-step>

<docs-step title="disabled xususiyatini bogʻlang">
**Submit** tugmasini oʻz ichiga olgan formaga murojaat qilish va hodisa bogʻlashini yaratish uchun `#actorForm` shablon murojaat oʻzgaruvchisidan foydalaning.

Formaning umumiy validligini bildiruvchi xususiyatini **Submit** tugmasining `disabled` xususiyatiga bogʻlaysiz.

<docs-code header="actor-form.component.html (submit-button)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="submit-button"/>
</docs-step>

<docs-step title="Ilovani ishga tushiring">
Tugma yoqilganiga eʼtibor bering — garchi u hali foydali hech narsa qilmasa ham.
</docs-step>

<docs-step title="Name qiymatini oʻchiring">
Bu "required" qoidasini buzadi, shuning uchun xato xabari koʻrsatiladi — va bu **Submit** tugmasini ham oʻchirib qoʻyishiga eʼtibor bering.

Tugmaning yoqilganlik holatini formaning validligiga qoʻlda bogʻlashingiz shart emas edi.
`FormsModule` kengaytirilgan forma elementida shablon murojaat oʻzgaruvchisini aniqlab, keyin tugma boshqaruv elementida oʻsha oʻzgaruvchiga murojaat qilganingizda buni avtomatik bajardi.
</docs-step>
</docs-workflow>

### Forma yuborilishiga javob berish {#respond-to-form-submission}

Forma yuborilishiga javobni koʻrsatish uchun maʼlumot kiritish hududini yashirib, uning oʻrniga boshqa narsa koʻrsatishingiz mumkin.

<docs-workflow>
<docs-step title="Formani oʻrang">
Butun formani `<div>` ichiga oʻrang va uning `hidden` xususiyatini `ActorFormComponent.submitted` xususiyatiga bogʻlang.

<docs-code header="actor-form.component.html (excerpt)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="edit-div"/>

Asosiy forma boshidan koʻrinadi, chunki `ActorFormComponent`'dan olingan ushbu parcha koʻrsatganidek, `submitted` xususiyati siz formani yubormaguningizcha false boʻladi:

<docs-code header="actor-form.component.ts (submitted)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.ts" region="submitted"/>

**Submit** tugmasini bosganingizda `submitted` bayrogʻi true boʻladi va forma yoʻqoladi.
</docs-step>

<docs-step title="Yuborilgan holatni qoʻshing">
Forma yuborilgan holatda boʻlganida boshqa narsa koʻrsatish uchun yangi `<div>` oʻrami ostiga quyidagi HTML'ni qoʻshing.

<docs-code header="actor-form.component.html (excerpt)" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="submitted"/>

Interpolyatsiya bogʻlashlari bilan faqat oʻqish uchun aktyorni koʻrsatuvchi bu `<div>` faqat komponent yuborilgan holatda boʻlganida paydo boʻladi.

Muqobil koʻrinishda bosish hodisasi `submitted` bayrogʻini tozalaydigan ifodaga bogʻlangan _Edit_ tugmasi bor.
</docs-step>

<docs-step title="Edit tugmasini sinab koʻring">
Koʻrinishni tahrirlanadigan formaga qaytarish uchun *Edit* tugmasini bosing.
</docs-step>
</docs-workflow>

## Xulosa {#summary}

Bu sahifada koʻrib chiqilgan Angular formasi maʼlumotlarni oʻzgartirish, validatsiya va boshqa imkoniyatlarni
taʼminlash uchun freymvorkning quyidagi imkoniyatlaridan foydalanadi.

- Angular HTML forma shabloni
- `@Component` dekoratoriga ega forma komponenti klassi
- `NgForm.ngSubmit` hodisa xususiyatiga bogʻlash orqali forma yuborilishiga ishlov berish
- `#actorForm` va `#name` kabi shablon murojaat oʻzgaruvchilari
- Ikki tomonlama maʼlumot bogʻlash uchun `[(ngModel)]` sintaksisi
- Validatsiya va forma elementi oʻzgarishlarini kuzatish uchun `name` atributlaridan foydalanish
- Input boshqaruv elementlaridagi murojaat oʻzgaruvchisining `valid` xususiyati boshqaruv elementi valid ekanini yoki xato xabarlarini koʻrsatishi kerakligini bildiradi
- `NgForm` validligiga bogʻlash orqali **Submit** tugmasining yoqilganlik holatini boshqarish
- Foydalanuvchilarga valid boʻlmagan boshqaruv elementlari haqida vizual qayta aloqa beruvchi maxsus CSS klasslari

Ilovaning yakuniy versiyasi kodi:

<docs-code-multifile>
    <docs-code header="actor-form.component.ts" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.ts" region="final"/>
    <docs-code header="actor-form.component.html" path="adev/src/content/examples/forms/src/app/actor-form/actor-form.component.html" region="final"/>
    <docs-code header="actor.ts" path="adev/src/content/examples/forms/src/app/actor.ts"/>
    <docs-code header="app.component.html" path="adev/src/content/examples/forms/src/app/app.component.html"/>
    <docs-code header="app.component.ts" path="adev/src/content/examples/forms/src/app/app.component.ts"/>
    <docs-code header="main.ts" path="adev/src/content/examples/forms/src/main.ts"/>
    <docs-code header="forms.css" path="adev/src/content/examples/forms/src/assets/forms.css"/>
</docs-code-multifile>
