# Reaktiv formalar

Reaktiv formalar qiymatlari vaqt oʻtishi bilan oʻzgaradigan forma input'larini boshqarishga modelga asoslangan yondashuvni taqdim etadi.
Bu qoʻllanma sizga asosiy forma boshqaruv elementini (form control) yaratish va yangilash, guruhda bir nechta boshqaruv elementlaridan foydalanish, forma qiymatlarini validatsiya qilish va ish vaqtida boshqaruv elementlarini qoʻshish yoki olib tashlash mumkin boʻlgan dinamik formalar yaratishni koʻrsatadi.

## Reaktiv formalarning umumiy koʻrinishi {#overview-of-reactive-forms}

Reaktiv formalar forma holatini maʼlum bir vaqt nuqtasida boshqarishga aniq va oʻzgarmas (immutable) yondashuvdan foydalanadi.
Forma holatidagi har bir oʻzgarish yangi holat qaytaradi, bu esa oʻzgarishlar orasida model yaxlitligini saqlaydi.
Reaktiv formalar observable oqimlar atrofida qurilgan boʻlib, bunda forma input'lari va qiymatlari sinxron tarzda murojaat qilish mumkin boʻlgan oqimlar sifatida taqdim etiladi.

Reaktiv formalar shuningdek, testlash uchun ham toʻgʻri yoʻl ochadi, chunki soʻralgan paytda maʼlumotlaringiz izchil va oldindan aytib boʻladigan boʻlishiga ishonchingiz komil boʻladi.
Bu oqimlarning har qanday isteʼmolchisi maʼlumotlarni xavfsiz tarzda oʻzgartirishi mumkin.

Reaktiv formalar [shablonga asoslangan formalardan](guide/forms/template-driven-forms) bir qancha jihatlari bilan farq qiladi.
Reaktiv formalar maʼlumotlar modeliga sinxron murojaat, observable operatorlari bilan oʻzgarmaslik va observable oqimlar orqali oʻzgarishlarni kuzatishni taʼminlaydi.

Shablonga asoslangan formalar shablonda maʼlumotlarni oʻzgartirish uchun bevosita murojaatga imkon beradi, lekin reaktiv formalarga qaraganda kamroq aniq, chunki ular shablonga joylashtirilgan direktivalarga, shuningdek, oʻzgarishlarni asinxron kuzatish uchun oʻzgaruvchan maʼlumotlarga tayanadi.
Ikki paradigmaning batafsil taqqoslanishi uchun [Formalar umumiy koʻrinishiga](guide/forms) qarang.

## Asosiy forma boshqaruv elementini qoʻshish {#adding-a-basic-form-control}

Forma boshqaruv elementlaridan foydalanish uchun uchta qadam bor.

1. Yangi komponent yarating va reaktiv formalar modulini roʻyxatdan oʻtkazing. Bu modul reaktiv formalardan foydalanish uchun zarur boʻlgan reaktiv forma direktivalarini eʼlon qiladi.
1. Yangi `FormControl` nusxasini yarating.
1. `FormControl` ni shablonda roʻyxatdan oʻtkazing.

Keyin komponentni shablonga qoʻshib formani koʻrsatishingiz mumkin.

Quyidagi misollar bitta forma boshqaruv elementini qanday qoʻshishni koʻrsatadi.
Misolda foydalanuvchi oʻz ismini input maydoniga kiritadi, bu input qiymati olinadi va forma boshqaruv elementining joriy qiymati koʻrsatiladi.

<docs-workflow>

<docs-step title="Yangi komponent yarating va ReactiveFormsModule'ni import qiling {#generate-a-new-component-and-import-the-reactiveformsmodule}">
Loyihangizda komponent yaratish uchun CLI'ning `ng generate component` buyrugʻidan foydalaning, `@angular/forms` paketidan `ReactiveFormsModule` ni import qiling va uni komponentingizning `imports` massiviga qoʻshing.

<docs-code header="name-editor.component.ts (excerpt)" path="adev/src/content/examples/reactive-forms/src/app/name-editor/name-editor.component.ts" region="imports" />
</docs-step>

<docs-step title="FormControl nusxasini eʼlon qiling {#declare-a-formcontrol-instance}">
Boshlangʻich qiymatini, bu holatda boʻsh satrni, oʻrnatish uchun `FormControl` konstruktoridan foydalaning. Bu boshqaruv elementlarini komponent klassingizda yaratish orqali siz forma input'ining holatini tinglash, yangilash va validatsiya qilish imkoniga darhol ega boʻlasiz.

<docs-code header="name-editor.component.ts" path="adev/src/content/examples/reactive-forms/src/app/name-editor/name-editor.component.ts" region="create-control"/>
</docs-step>

<docs-step title="Boshqaruv elementini shablonda roʻyxatdan oʻtkazing {#register-the-control-in-the-template}">
Boshqaruv elementini komponent klassida yaratganingizdan soʻng, uni shablondagi forma boshqaruv elementi bilan bogʻlashingiz kerak. `FormControlDirective` tomonidan taqdim etiladigan va `ReactiveFormsModule` ga ham kiritilgan `formControl` bogʻlashidan foydalanib, shablonni forma boshqaruv elementi bilan yangilang.

<docs-code header="name-editor.component.html" path="adev/src/content/examples/reactive-forms/src/app/name-editor/name-editor.component.html" region="control-binding" />

Shablon bogʻlash sintaksisidan foydalanib, forma boshqaruv elementi endi shablondagi `name` input elementida roʻyxatdan oʻtkazildi. Forma boshqaruv elementi va DOM elementi bir-biri bilan muloqot qiladi: view modeldagi oʻzgarishlarni aks ettiradi, model esa view'dagi oʻzgarishlarni aks ettiradi.
</docs-step>

<docs-step title="Komponentni koʻrsating {#display-the-component}">
`name` xususiyatiga biriktirilgan `FormControl` `<app-name-editor>` komponenti shablonga qoʻshilganda koʻrsatiladi.

<docs-code header="app.component.html (name editor)" path="adev/src/content/examples/reactive-forms/src/app/app.component.1.html" region="app-name-editor"/>
</docs-step>
</docs-workflow>

### Forma boshqaruv elementi qiymatini koʻrsatish {#displaying-a-form-control-value}

Qiymatni quyidagi usullar bilan koʻrsatishingiz mumkin:

- `valueChanges` observable'i orqali, bunda forma qiymatidagi oʻzgarishlarni shablonda `AsyncPipe` yordamida yoki komponent klassida `subscribe()` metodi yordamida tinglashingiz mumkin
- Joriy qiymatning oniy holatini (snapshot) beradigan `value` xususiyati bilan

Quyidagi misol shablonda interpolyatsiya yordamida joriy qiymatni qanday koʻrsatishni koʻrsatadi.

<docs-code header="name-editor.component.html (control value)" path="adev/src/content/examples/reactive-forms/src/app/name-editor/name-editor.component.html" region="display-value"/>

Forma boshqaruv elementini yangilaganingizda koʻrsatilgan qiymat ham oʻzgaradi.

Reaktiv formalar har bir nusxa bilan taqdim etiladigan xususiyatlar va metodlar orqali berilgan boshqaruv elementi haqidagi maʼlumotlarga murojaat qilish imkonini beradi.
Asosiy [AbstractControl](api/forms/AbstractControl 'API reference') klassining bu xususiyatlari va metodlari forma holatini boshqarish va [input validatsiyasi](#validating-form-input 'Learn more about validating form input') bilan ishlashda xabarlarni qachon koʻrsatishni aniqlash uchun ishlatiladi.

`FormControl` ning boshqa xususiyatlari va metodlari haqida [API maʼlumotnomasida](api/forms/FormControl 'Detailed syntax reference') oʻqing.

### Forma boshqaruv elementi qiymatini almashtirish {#replacing-a-form-control-value}

Reaktiv formalar boshqaruv elementi qiymatini programmatik tarzda oʻzgartirish uchun metodlarga ega, bu sizga qiymatni foydalanuvchi ishtirokisiz yangilash imkonini beradi.
Forma boshqaruv elementi nusxasi forma boshqaruv elementining qiymatini yangilaydigan va berilgan qiymat tuzilmasini boshqaruv elementi tuzilmasiga nisbatan validatsiya qiladigan `setValue()` metodini taqdim etadi.
Masalan, forma maʼlumotlarini backend API yoki servisdan olganda, boshqaruv elementini yangi qiymatiga yangilash va eski qiymatni butunlay almashtirish uchun `setValue()` metodidan foydalaning.

Quyidagi misol komponent klassiga `setValue()` metodi yordamida boshqaruv elementi qiymatini _Nancy_ ga yangilaydigan metod qoʻshadi.

<docs-code header="name-editor.component.ts (update value)" path="adev/src/content/examples/reactive-forms/src/app/name-editor/name-editor.component.ts" region="update-value"/>

Ism yangilanishini simulyatsiya qilish uchun shablonga tugma qoʻshing.
**Update Name** tugmasini bosganingizda, forma boshqaruv elementiga kiritilgan qiymat uning joriy qiymati sifatida aks etadi.

<docs-code header="name-editor.component.html (update value)" path="adev/src/content/examples/reactive-forms/src/app/name-editor/name-editor.component.html" region="update-value"/>

Forma modeli boshqaruv elementi uchun haqiqat manbai hisoblanadi, shuning uchun tugmani bosganingizda input qiymati komponent klassi ichida oʻzgartiriladi va uning joriy qiymati qayta yoziladi.

HELPFUL: Bu misolda siz bitta boshqaruv elementidan foydalanyapsiz.
`setValue()` metodini [forma guruhi](#grouping-form-controls) yoki [forma massivi](#creating-dynamic-forms) nusxasi bilan ishlatganda qiymat guruh yoki massiv tuzilmasiga mos kelishi kerak.

## Forma boshqaruv elementlarini guruhlash {#grouping-form-controls}

Formalar odatda bir nechta oʻzaro bogʻliq boshqaruv elementlarini oʻz ichiga oladi.
Reaktiv formalar bir nechta oʻzaro bogʻliq boshqaruv elementlarini bitta kirish formasiga guruhlashning ikki usulini taqdim etadi.

| Forma guruhlari | Tafsilotlar                                                                                                                                                                                                                                                |
| :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Forma guruhi  | Birgalikda boshqarishingiz mumkin boʻlgan qatʼiy belgilangan boshqaruv elementlari toʻplamiga ega formani belgilaydi. Forma guruhi asoslari ushbu boʻlimda muhokama qilinadi. Murakkabroq formalar yaratish uchun [forma guruhlarini ichma-ich joylashtirishingiz](#creating-nested-form-groups 'See more about nesting groups') ham mumkin. |
| Forma massivi  | Ish vaqtida boshqaruv elementlarini qoʻshish va olib tashlash mumkin boʻlgan dinamik formani belgilaydi. Murakkabroq formalar yaratish uchun forma massivlarini ichma-ich joylashtirishingiz ham mumkin. Bu variant haqida koʻproq bilish uchun [Dinamik formalar yaratish](#creating-dynamic-forms) boʻlimiga qarang.                              |

Forma boshqaruv elementi nusxasi sizga bitta input maydoni ustidan nazoratni bergani kabi, forma guruhi nusxasi forma boshqaruv elementlari nusxalari guruhining \(masalan, formaning\) forma holatini kuzatib boradi.
Forma guruhi nusxasidagi har bir boshqaruv elementi forma guruhi yaratilayotganda nomi boʻyicha kuzatiladi.
Quyidagi misol bitta guruhda bir nechta forma boshqaruv elementi nusxalarini qanday boshqarishni koʻrsatadi.

`ProfileEditor` komponentini yarating va `@angular/forms` paketidan `FormGroup` va `FormControl` klasslarini import qiling.

```shell
ng generate component ProfileEditor
```

<docs-code header="profile-editor.component.ts (imports)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="imports"/>

Bu komponentga forma guruhini qoʻshish uchun quyidagi qadamlarni bajaring.

1. `FormGroup` nusxasini yarating.
1. `FormGroup` modelini va view'ni bogʻlang.
1. Forma maʼlumotlarini saqlang.

<docs-workflow>

<docs-step title="FormGroup nusxasini yarating {#create-a-formgroup-instance}">
Komponent klassida `profileForm` nomli xususiyat yarating va bu xususiyatga yangi forma guruhi nusxasini oʻrnating. Forma guruhini ishga tushirish uchun konstruktorga nomlangan kalitlari oʻz boshqaruv elementlariga moslashtirilgan obyektni bering.

Profil formasi uchun `firstName` va `lastName` nomli ikkita forma boshqaruv elementi nusxasini qoʻshing

<docs-code header="profile-editor.component.ts (form group)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="formgroup"/>

Alohida forma boshqaruv elementlari endi guruh ichida jamlangan. `FormGroup` nusxasi oʻz model qiymatini guruhdagi har bir boshqaruv elementi qiymatlaridan yigʻilgan obyekt sifatida taqdim etadi. Forma guruhi nusxasi forma boshqaruv elementi nusxasi bilan bir xil xususiyatlarga (masalan, `value` va `untouched`) va metodlarga (masalan, `setValue()`) ega.
</docs-step>

<docs-step title="FormGroup modelini va view'ni bogʻlang {#associate-the-formgroup-model-and-view}">
Forma guruhi oʻzining har bir boshqaruv elementining holati va oʻzgarishlarini kuzatib boradi, shuning uchun boshqaruv elementlaridan biri oʻzgarsa, ota boshqaruv elementi ham yangi holat yoki qiymat oʻzgarishini chiqaradi. Guruh modeli uning aʼzolaridan tashkil topadi. Modelni belgilaganingizdan soʻng, modelni view'da aks ettirish uchun shablonni yangilashingiz kerak.

<docs-code header="profile-editor.component.html (template form group)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.html" region="formgroup"/>

Forma guruhi boshqaruv elementlari guruhini oʻz ichiga olgani kabi, _profileForm_ `FormGroup` `FormGroup` direktivasi bilan `form` elementiga bogʻlanadi va model bilan input'larni oʻz ichiga olgan forma oʻrtasida muloqot qatlamini yaratadi. `FormControlName` direktivasi tomonidan taqdim etiladigan `formControlName` input'i har bir alohida input'ni `FormGroup` da belgilangan forma boshqaruv elementiga bogʻlaydi. Forma boshqaruv elementlari oʻzlariga tegishli elementlar bilan muloqot qiladi. Ular shuningdek, oʻzgarishlarni model qiymati uchun haqiqat manbai boʻlgan forma guruhi nusxasiga ham yetkazadi.
</docs-step>

<docs-step title="Forma maʼlumotlarini saqlang {#save-form-data}">
`ProfileEditor` komponenti foydalanuvchidan kiritilgan maʼlumotlarni qabul qiladi, lekin haqiqiy stsenariyda siz forma qiymatini olib, uni komponentdan tashqarida keyingi qayta ishlash uchun taqdim etishni istaysiz. `FormGroup` direktivasi `form` elementi tomonidan chiqariladigan `submit` hodisasini tinglaydi va callback funksiyasiga bogʻlashingiz mumkin boʻlgan `ngSubmit` hodisasini chiqaradi. `form` tegiga `onSubmit()` callback metodi bilan `ngSubmit` hodisa tinglovchisini qoʻshing.

<docs-code header="profile-editor.component.html (submit event)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.html" region="ng-submit"/>

`ProfileEditor` komponentidagi `onSubmit()` metodi `profileForm` ning joriy qiymatini oladi. Formani inkapsulyatsiyalangan holda saqlash va forma qiymatini komponentdan tashqariga taqdim etish uchun `output()` dan foydalaning. Quyidagi misol brauzer konsoliga xabar chiqarish uchun `console.warn` dan foydalanadi.

<docs-code header="profile-editor.component.ts (submit method)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="on-submit"/>

`submit` hodisasi `form` tegi tomonidan oʻrnatilgan DOM hodisasi yordamida chiqariladi. Siz hodisani `submit` turidagi tugmani bosish orqali ishga tushirasiz. Bu foydalanuvchiga toʻldirilgan formani yuborish uchun **Enter** tugmasini bosish imkonini beradi.

Formani yuborishni ishga tushirish uchun forma pastiga tugma qoʻshishda `button` elementidan foydalaning.

<docs-code header="profile-editor.component.html (submit button)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.html" region="submit-button"/>

Yuqoridagi parchadagi tugmada `profileForm` yaroqsiz boʻlganda tugmani oʻchirib qoʻyish uchun `disabled` bogʻlashi ham biriktirilgan. Siz hali hech qanday validatsiya qilmayapsiz, shuning uchun tugma har doim yoqilgan boʻladi. Asosiy forma validatsiyasi [Forma input'ini validatsiya qilish](#validating-form-input) boʻlimida yoritilgan.
</docs-step>

<docs-step title="Komponentni koʻrsating {#display-the-component-form-group}">
Formani oʻz ichiga olgan `ProfileEditor` komponentini koʻrsatish uchun uni komponent shabloniga qoʻshing.

<docs-code header="app.component.html (profile editor)" path="adev/src/content/examples/reactive-forms/src/app/app.component.1.html" region="app-profile-editor"/>

`ProfileEditor` forma guruhi nusxasi ichidagi `firstName` va `lastName` boshqaruv elementlari uchun forma boshqaruv elementi nusxalarini boshqarish imkonini beradi.
</docs-step>
</docs-workflow>

### Ichma-ich forma guruhlarini yaratish {#creating-nested-form-groups}

Forma guruhlari bola sifatida alohida forma boshqaruv elementi nusxalarini ham, boshqa forma guruhi nusxalarini ham qabul qilishi mumkin.
Bu murakkab forma modellarini tuzishni, ularga xizmat koʻrsatishni va mantiqiy guruhlashni osonlashtiradi.

Murakkab formalar yaratishda maʼlumotlarning turli sohalarini kichikroq boʻlimlarda boshqarish osonroq.
Ichma-ich forma guruhi nusxasidan foydalanish katta forma guruhlarini kichikroq, boshqarish osonroq guruhlarga ajratish imkonini beradi.

Murakkabroq formalar yaratish uchun quyidagi qadamlardan foydalaning.

1. Ichki guruh yarating.
1. Ichki formani shablonda guruhlang.

Baʼzi maʼlumot turlari tabiiy ravishda bir guruhga tushadi.
Ism va manzil bunday ichki guruhlarning odatiy misollari boʻlib, quyidagi misollarda ishlatiladi.

<docs-workflow>
<docs-step title="Ichki guruh yarating {#create-a-nested-group}">
`profileForm` da ichki guruh yaratish uchun forma guruhi nusxasiga ichki `address` elementini qoʻshing.

<docs-code header="profile-editor.component.ts (nested form group)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="nested-formgroup"/>

Bu misolda `address group` joriy `firstName` va `lastName` boshqaruv elementlarini yangi `street`, `city`, `state` va `zip` boshqaruv elementlari bilan birlashtiradi. Forma guruhidagi `address` elementi forma guruhidagi umumiy `profileForm` elementining bolasi boʻlsa-da, qiymat va holat oʻzgarishlarida bir xil qoidalar amal qiladi. Ichki forma guruhidagi holat va qiymat oʻzgarishlari ota forma guruhiga tarqaladi va umumiy model bilan izchillikni saqlaydi.
</docs-step>

<docs-step title="Ichki formani shablonda guruhlang {#group-the-nested-form-in-the-template}">
Komponent klassida modelni yangilaganingizdan soʻng, forma guruhi nusxasi va uning input elementlarini ulash uchun shablonni yangilang. `street`, `city`, `state` va `zip` maydonlarini oʻz ichiga olgan `address` forma guruhini `ProfileEditor` shabloniga qoʻshing.

<docs-code header="profile-editor.component.html (template nested form group)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.html" region="formgroupname"/>

`ProfileEditor` formasi bitta guruh sifatida koʻrsatiladi, lekin model mantiqiy guruhlash sohalarini ifodalash uchun yanada boʻlinadi.

Komponent shablonida forma guruhi nusxasining qiymatini `value` xususiyati va `JsonPipe` yordamida koʻrsating.
</docs-step>
</docs-workflow>

### Maʼlumotlar modelining qismlarini yangilash {#updating-parts-of-the-data-model}

Bir nechta boshqaruv elementlarini oʻz ichiga olgan forma guruhi nusxasining qiymatini yangilashda siz modelning faqat qismlarini yangilashni istashingiz mumkin.
Bu boʻlim forma boshqaruv elementi maʼlumotlar modelining muayyan qismlarini qanday yangilashni yoritadi.

Model qiymatini yangilashning ikki usuli bor:

| Metodlar        | Tafsilotlar                                                                                                                                                               |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `setValue()`   | Alohida boshqaruv elementi uchun yangi qiymat oʻrnatadi. `setValue()` metodi forma guruhi tuzilmasiga qatʼiy rioya qiladi va boshqaruv elementining butun qiymatini almashtiradi. |
| `patchValue()` | Forma modelida oʻzgargan, obyektda belgilangan har qanday xususiyatlarni almashtiradi.                                                                                     |

`setValue()` metodining qatʼiy tekshiruvlari murakkab formalarda ichma-ich joylashish xatolarini aniqlashga yordam beradi, `patchValue()` esa bunday xatolarda jimgina ishdan chiqadi.

`ProfileEditorComponent` da foydalanuvchining ismi va koʻcha manzilini yangilash uchun quyidagi misol bilan `updateProfile` metodidan foydalaning.

<docs-code header="profile-editor.component.ts (patch value)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="patch-value"/>

Foydalanuvchi profilini talab boʻyicha yangilash uchun shablonga tugma qoʻshib yangilanishni simulyatsiya qiling.

<docs-code header="profile-editor.component.html (update value)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.html" region="patch-value"/>

Foydalanuvchi tugmani bosganda `profileForm` modeli `firstName` va `street` uchun yangi qiymatlar bilan yangilanadi. `street` ning `address` xususiyati ichidagi obyektda berilganiga eʼtibor bering.
Bu zarur, chunki `patchValue()` metodi yangilanishni model tuzilmasiga nisbatan qoʻllaydi.
`patchValue()` faqat forma modeli belgilagan xususiyatlarni yangilaydi.

## Boshqaruv elementlarini yaratish uchun FormBuilder servisidan foydalanish {#using-the-formbuilder-service-to-generate-controls}

Bir nechta formalar bilan ishlashda forma boshqaruv elementi nusxalarini qoʻlda yaratish takroriy boʻlib qolishi mumkin.
`FormBuilder` servisi boshqaruv elementlarini yaratish uchun qulay metodlarni taqdim etadi.

Bu servisdan foydalanish uchun quyidagi qadamlarni bajaring.

1. `FormBuilder` klassini import qiling.
1. `FormBuilder` servisini inyeksiya qiling.
1. Forma tarkibini yarating.

Quyidagi misollar forma boshqaruv elementi va forma guruhi nusxalarini yaratish uchun form builder servisidan foydalanishga `ProfileEditor` komponentini qanday refaktoring qilishni koʻrsatadi.

<docs-workflow>
<docs-step title="FormBuilder klassini import qiling {#import-the-formbuilder-class}">
`@angular/forms` paketidan `FormBuilder` klassini import qiling.

<docs-code header="profile-editor.component.ts (import)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="form-builder-imports"/>

</docs-step>

<docs-step title="FormBuilder servisini inyeksiya qiling {#inject-the-formbuilder-service}">
`FormBuilder` servisi reaktiv formalar modulidan inyeksiya qilinadigan provider hisoblanadi. Bu bogʻliqlikni komponentingizga inyeksiya qilish uchun `inject()` funksiyasidan foydalaning.

<docs-code header="profile-editor.component.ts (property init)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="inject-form-builder"/>

</docs-step>
<docs-step title="Forma boshqaruv elementlarini yarating {#generate-form-controls}">
`FormBuilder` servisi uchta metodga ega: `control()`, `group()` va `array()`. Bular komponent klasslaringizda forma boshqaruv elementlari, forma guruhlari va forma massivlarini oʻz ichiga olgan nusxalarni yaratish uchun fabrika metodlaridir. `profileForm` boshqaruv elementlarini yaratish uchun `group` metodidan foydalaning.

<docs-code header="profile-editor.component.ts (form builder)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="form-builder"/>

Yuqoridagi misolda modeldagi xususiyatlarni belgilash uchun `group()` metodini xuddi shu obyekt bilan ishlatasiz. Har bir boshqaruv elementi nomi uchun qiymat — massivning birinchi elementi sifatida boshlangʻich qiymatni oʻz ichiga olgan massiv.

TIP: Boshqaruv elementini faqat boshlangʻich qiymat bilan belgilashingiz mumkin, lekin boshqaruv elementlaringizga sinxron yoki asinxron validatsiya kerak boʻlsa, massivning ikkinchi va uchinchi elementlari sifatida sinxron va asinxron validatorlarni qoʻshing. Form builder'dan foydalanishni nusxalarni qoʻlda yaratish bilan taqqoslang.

  <docs-code-multifile>
    <docs-code header="profile-editor.component.ts (instances)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="formgroup-compare"/>
    <docs-code header="profile-editor.component.ts (form builder)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="formgroup-compare"/>
  </docs-code-multifile>
</docs-step>

</docs-workflow>

## Forma input'ini validatsiya qilish {#validating-form-input}

_Forma validatsiyasi_ foydalanuvchi kiritgan maʼlumotlarning toʻliq va toʻgʻri boʻlishini taʼminlash uchun ishlatiladi.
Bu boʻlim forma boshqaruv elementiga bitta validator qoʻshish va formaning umumiy holatini koʻrsatishni yoritadi.
Forma validatsiyasi [Forma validatsiyasi](guide/forms/form-validation) qoʻllanmasida kengroq yoritilgan.

Forma validatsiyasini qoʻshish uchun quyidagi qadamlardan foydalaning.

1. Forma komponentingizga validator funksiyasini import qiling.
1. Validatorni formadagi maydonga qoʻshing.
1. Validatsiya holatini boshqarish uchun mantiq qoʻshing.

Eng keng tarqalgan validatsiya — maydonni majburiy qilish.
Quyidagi misol `firstName` boshqaruv elementiga majburiylik validatsiyasini qanday qoʻshishni va validatsiya natijasini koʻrsatishni koʻrsatadi.

<docs-workflow>
<docs-step title="Validator funksiyasini import qiling {#import-a-validator-function}">
Reaktiv formalar keng tarqalgan holatlar uchun validator funksiyalari toʻplamini oʻz ichiga oladi. Bu funksiyalar validatsiya qilinadigan boshqaruv elementini qabul qiladi va validatsiya tekshiruvi asosida xato obyekti yoki null qiymatini qaytaradi.

`@angular/forms` paketidan `Validators` klassini import qiling.

<docs-code header="profile-editor.component.ts (import)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="validator-imports"/>
</docs-step>

<docs-step title="Maydonni majburiy qiling {#make-a-field-required}">
`ProfileEditor` komponentida `firstName` boshqaruv elementi uchun massivning ikkinchi elementi sifatida `Validators.required` statik metodini qoʻshing.

<docs-code header="profile-editor.component.ts (required validator)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="required-validator"/>
</docs-step>

<docs-step title="Forma holatini koʻrsating {#display-form-status}">
Forma boshqaruv elementiga majburiy maydon qoʻshganingizda uning boshlangʻich holati yaroqsiz (invalid) boʻladi. Bu yaroqsiz holat ota forma guruhi elementiga tarqaladi va uning holatini ham yaroqsiz qiladi. Forma guruhi nusxasining joriy holatiga uning `status` xususiyati orqali murojaat qiling.

`profileForm` ning joriy holatini interpolyatsiya yordamida koʻrsating.

<docs-code header="profile-editor.component.html (display status)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.html" region="display-status"/>

**Submit** tugmasi oʻchirib qoʻyilgan, chunki majburiy `firstName` forma boshqaruv elementi sababli `profileForm` yaroqsiz. `firstName` input'ini toʻldirganingizdan soʻng forma yaroqli boʻladi va **Submit** tugmasi yoqiladi.

Forma validatsiyasi haqida koʻproq bilish uchun [Forma validatsiyasi](guide/forms/form-validation) qoʻllanmasiga murojaat qiling.
</docs-step>
</docs-workflow>

## Dinamik formalar yaratish {#creating-dynamic-forms}

`FormArray` — istalgan sondagi nomsiz boshqaruv elementlarini boshqarish uchun `FormGroup` ga muqobil.
Forma guruhi nusxalaridagi kabi, forma massivi nusxalariga boshqaruv elementlarini dinamik tarzda qoʻshishingiz va olib tashlashingiz mumkin, forma massivi nusxasining qiymati va validatsiya holati esa uning bola boshqaruv elementlaridan hisoblanadi.
Biroq, har bir boshqaruv elementi uchun nom boʻyicha kalit belgilashingiz shart emas, shuning uchun bola qiymatlar sonini oldindan bilmasangiz, bu ajoyib variant.

Dinamik formani belgilash uchun quyidagi qadamlarni bajaring.

1. `FormArray` klassini import qiling.
1. `FormArray` boshqaruv elementini belgilang.
1. `FormArray` boshqaruv elementiga getter metodi orqali murojaat qiling.
1. Forma massivini shablonda koʻrsating.

Quyidagi misol `ProfileEditor` da _taxalluslar_ (aliases) massivini qanday boshqarishni koʻrsatadi.

<docs-workflow>
<docs-step title="`FormArray` klassini import qiling {#import-the-formarray-class}">
Tip maʼlumoti uchun foydalanish maqsadida `@angular/forms` dan `FormArray` klassini import qiling. `FormBuilder` servisi `FormArray` nusxasini yaratishga tayyor.

<docs-code header="profile-editor.component.ts (import)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="form-array-imports"/>
</docs-step>

<docs-step title="`FormArray` boshqaruv elementini belgilang {#define-a-formarray-control}">
Forma massivini massivda belgilash orqali noldan koʻpgacha istalgan sondagi boshqaruv elementlari bilan ishga tushirishingiz mumkin. Forma massivini belgilash uchun `profileForm` forma guruhi nusxasiga `aliases` xususiyatini qoʻshing.

Massivni belgilash uchun `FormBuilder.array()` metodidan, massivni boshlangʻich boshqaruv elementi bilan toʻldirish uchun esa `FormBuilder.control()` metodidan foydalaning.

<docs-code header="profile-editor.component.ts (aliases form array)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="aliases"/>

Forma guruhi nusxasidagi aliases boshqaruv elementi endi dinamik tarzda koʻproq boshqaruv elementlari qoʻshilmaguncha bitta boshqaruv elementi bilan toʻldirilgan.
</docs-step>

<docs-step title="`FormArray` boshqaruv elementiga murojaat qiling {#access-the-formarray-control}">
Har bir nusxani olish uchun `profileForm.get()` metodini takrorlash oʻrniga getter forma massivi nusxasidagi taxalluslarga murojaat qilish imkonini beradi. Forma massivi nusxasi massivdagi noaniq sondagi boshqaruv elementlarini ifodalaydi. Boshqaruv elementiga getter orqali murojaat qilish qulay va bu yondashuvni qoʻshimcha boshqaruv elementlari uchun takrorlash oson. <br />

Ota forma guruhidan taxalluslar forma massivi boshqaruv elementini olish uchun getter sintaksisidan foydalanib `aliases` klass xususiyatini yarating.

<docs-code header="profile-editor.component.ts (aliases getter)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="aliases-getter"/>

Qaytarilgan boshqaruv elementi `AbstractControl` tipida boʻlgani uchun forma massivi nusxasining metod sintaksisiga murojaat qilish uchun aniq tip koʻrsatishingiz kerak. Taxalluslar forma massiviga taxallus boshqaruv elementini dinamik tarzda qoʻshish uchun metod belgilang. `FormArray.push()` metodi boshqaruv elementini massivga yangi element sifatida qoʻshadi, shuningdek, bir vaqtning oʻzida bir nechta boshqaruv elementini roʻyxatdan oʻtkazish uchun FormArray.push() ga boshqaruv elementlari massivini ham uzatishingiz mumkin.

<docs-code header="profile-editor.component.ts (add alias)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="add-alias"/>

Shablonda har bir boshqaruv elementi alohida input maydoni sifatida koʻrsatiladi.

</docs-step>

<docs-step title="Forma massivini shablonda koʻrsating {#display-the-form-array-in-the-template}">

Forma modelingizdagi taxalluslarni biriktirish uchun ularni shablonga qoʻshishingiz kerak. `FormGroupName` tomonidan taqdim etiladigan `formGroupName` input'iga oʻxshab, `formArrayName` `FormArrayName` yordamida forma massivi nusxasidan shablonga muloqotni bogʻlaydi.

`formGroupName` elementini yopuvchi `<div>` dan keyin quyidagi shablon HTML'ini qoʻshing.

<docs-code header="profile-editor.component.html (aliases form array template)" path="adev/src/content/examples/reactive-forms/src/app/profile-editor/profile-editor.component.html" region="formarrayname"/>

`@for` bloki aliases forma massivi nusxasi tomonidan taqdim etilgan har bir forma boshqaruv elementi nusxasi boʻylab iteratsiya qiladi. Forma massivi elementlari nomsiz boʻlgani uchun indeksni `i` oʻzgaruvchisiga biriktirasiz va uni `formControlName` input'iga bogʻlash uchun har bir boshqaruv elementiga uzatasiz.

Har safar yangi taxallus nusxasi qoʻshilganda yangi forma massivi nusxasiga indeks asosida oʻz boshqaruv elementi beriladi. Bu ildiz boshqaruv elementining holati va qiymatini hisoblashda har bir alohida boshqaruv elementini kuzatish imkonini beradi.

NOTE: Zoneless ilovalarda reaktiv formalar modelini oʻzgartirish (masalan, `FormArray.push()` ni chaqirish) komponentning oʻzgarishlarni aniqlashini avtomatik ravishda rejalashtirmaydi. Agar shabloningiz `aliases.controls` kabi tuzilmaviy model oʻzgarishlariga bogʻliq boʻlsa, komponent Angular'ga oʻzgarishlarni aniqlashni ishga tushirish kerakligini bildirishiga ishonch hosil qiling, masalan, formalar observable'ini `ChangeDetectorRef.markForCheck()` ga ulash orqali:

```ts
import {ChangeDetectorRef, Component, inject} from '@angular/core';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';

@Component({/* ... */})
export class ProfileEditor {
  private readonly cdr = inject(ChangeDetectorRef);

  constructor() {
    this.profileForm.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe(() => this.cdr.markForCheck());
  }
}
```

</docs-step>

### Yuqori darajadagi forma massivlari uchun `FormArrayDirective` dan foydalanish {#using-formarraydirective-for-top-level-form-arrays}

`FormArrayDirective` yordamida `FormArray` ni bevosita `<form>` elementiga bogʻlashingiz mumkin.  
Bu forma yuqori darajadagi `FormGroup` dan foydalanmaganda va massivning oʻzi toʻliq forma modelini ifodalaganda foydali.

```angular-ts
import {Component} from '@angular/core';
import {FormArray, FormControl} from '@angular/forms';

@Component({
  selector: 'form-array-example',
  template: `
    <form [formArray]="form">
      @for (control of form.controls; track $index) {
        <input [formControlName]="$index" />
      }
    </form>
  `,
})
export class FormArrayExampleComponent {
  controls = [new FormControl('fish'), new FormControl('cat'), new FormControl('dog')];

  form = new FormArray(this.controls);
}
```

<docs-step title="Taxallus qoʻshing {#add-an-alias}">

Dastlab forma bitta `Alias` maydonini oʻz ichiga oladi. Yana bir maydon qoʻshish uchun **Add Alias** tugmasini bosing. Shuningdek, shablon pastidagi `Form Value` da koʻrsatilgan forma modeli xabar qilgan taxalluslar massivini ham tekshirishingiz mumkin. Har bir taxallus uchun forma boshqaruv elementi nusxasi oʻrniga qoʻshimcha maydonlarga ega boshqa forma guruhi nusxasini tuzishingiz mumkin. Har bir element uchun boshqaruv elementini belgilash jarayoni bir xil.
</docs-step>

</docs-workflow>

## Boshqaruv elementi holati oʻzgarishining yagona hodisalari {#unified-control-state-change-events}

Barcha forma boshqaruv elementlari `AbstractControl` (`FormControl`, `FormGroup`, `FormArray` va `FormRecord`) dagi `events` observable'i orqali **boshqaruv elementi holati oʻzgarishi hodisalarining** yagona birlashtirilgan oqimini taqdim etadi.
Bu yagona oqim **value**, **status**, **pristine**, **touched** va **reset** holat oʻzgarishlariga, shuningdek, **submit** kabi **forma darajasidagi harakatlarga** reaksiya bildirish imkonini beradi va bir nechta observable'larni ulash oʻrniga barcha yangilanishlarni bitta obuna bilan boshqarish imkonini beradi.

### Hodisa turlari {#event-types}

`events` tomonidan chiqarilgan har bir element muayyan hodisa klassining nusxasi hisoblanadi:

- **`ValueChangeEvent`** — boshqaruv elementining **qiymati** oʻzgarganda.
- **`StatusChangeEvent`** — boshqaruv elementining **validatsiya holati** `FormControlStatus` qiymatlaridan biriga (`VALID`, `INVALID`, `PENDING` yoki `DISABLED`) yangilanganda.
- **`PristineChangeEvent`** — boshqaruv elementining **pristine/dirty** holati oʻzgarganda.
- **`TouchedChangeEvent`** — boshqaruv elementining **touched/untouched** holati oʻzgarganda.
- **`FormResetEvent`** — boshqaruv elementi yoki forma `reset()` API'si yoki tabiiy harakat orqali qayta tiklanganda.
- **`FormSubmittedEvent`** — forma yuborilganda.

Barcha hodisa klasslari `ControlEvent` dan meros oladi va oʻzgarishni boshlagan `AbstractControl` ga `source` havolasini oʻz ichiga oladi, bu katta formalarda foydali.

```ts
import {Component} from '@angular/core';
import {
  FormControl,
  ValueChangeEvent,
  StatusChangeEvent,
  PristineChangeEvent,
  TouchedChangeEvent,
  FormResetEvent,
  FormSubmittedEvent,
  ReactiveFormsModule,
  FormGroup,
} from '@angular/forms';

@Component(/* ... */)
export class UnifiedEventsBasicComponent {
  form = new FormGroup({
    username: new FormControl(''),
  });

  constructor() {
    this.form.events.subscribe((e) => {
      if (e instanceof ValueChangeEvent) {
        console.log('Value changed to: ', e.value);
      }

      if (e instanceof StatusChangeEvent) {
        console.log('Status changed to: ', e.status);
      }

      if (e instanceof PristineChangeEvent) {
        console.log('Pristine status changed to: ', e.pristine);
      }

      if (e instanceof TouchedChangeEvent) {
        console.log('Touched status changed to: ', e.touched);
      }

      if (e instanceof FormResetEvent) {
        console.log('Form was reset');
      }

      if (e instanceof FormSubmittedEvent) {
        console.log('Form was submitted');
      }
    });
  }
}
```

### Muayyan hodisalarni filtrlash {#filtering-specific-events}

Sizga hodisa turlarining faqat bir qismi kerak boʻlganda RxJS operatorlarini afzal koʻring.

```ts
import {filter} from 'rxjs/operators';
import {StatusChangeEvent} from '@angular/forms';

control.events
  .pipe(filter((e) => e instanceof StatusChangeEvent))
  .subscribe((e) => console.log('Status:', e.status));
```

### Bir nechta obunani birlashtirish {#unifying-from-multiple-subscriptions}

**Oldin**

```ts
import {combineLatest} from 'rxjs';

combineLatest([control.valueChanges, control.statusChanges]).subscribe(([value, status]) => {
  /* ... */
});
```

**Keyin**

```ts
control.events.subscribe((e) => {
  // Handle ValueChangeEvent, StatusChangeEvent, etc.
});
```

NOTE: Qiymat oʻzgarganda hodisa bu boshqaruv elementining qiymati yangilangandan keyin darhol chiqariladi. Ota boshqaruv elementining qiymati (masalan, agar bu FormControl FormGroup ning bir qismi boʻlsa) keyinroq yangilanadi, shuning uchun bu hodisaning callback'idan ota boshqaruv elementining qiymatiga (`value` xususiyati orqali) murojaat qilish hali yangilanmagan qiymatni olishga olib kelishi mumkin. Buning oʻrniga ota boshqaruv elementining `events` iga obuna boʻling.

## Forma boshqaruv elementi holatini boshqarish {#managing-form-control-state}

Reaktiv formalar boshqaruv elementi holatini **touched/untouched** va **pristine/dirty** orqali kuzatadi. Angular DOM bilan oʻzaro taʼsir paytida bularni avtomatik yangilaydi, lekin siz ularni programmatik tarzda ham boshqarishingiz mumkin.

**[`markAsTouched`](api/forms/FormControl#markAsTouched)** — boshqaruv elementi yoki formani qiymatni oʻzgartirmaydigan focus va blur hodisalari orqali touched deb belgilaydi. Sukut boʻyicha ota boshqaruv elementlariga tarqaladi.

```ts
// Show validation errors after user leaves a field
onEmailBlur() {
  const email = this.form.get('email');
  email.markAsTouched();
}
```

**[`markAsUntouched`](api/forms/FormControl#markAsUntouched)** — boshqaruv elementi yoki formani untouched deb belgilaydi. Barcha bola boshqaruv elementlariga kaskad tarzda tarqaladi va barcha ota boshqaruv elementlarining touched holatini qayta hisoblaydi.

```ts
// Reset form state after successful submission
onSubmitSuccess() {
  this.form.markAsUntouched();
  this.form.markAsPristine();
}
```

**[`markAsDirty`](api/forms/FormControl#markAsDirty)** — boshqaruv elementi yoki formani dirty deb belgilaydi, yaʼni qiymat oʻzgartirilgan. Sukut boʻyicha ota boshqaruv elementlariga tarqaladi.

```ts
// Mark programmatically changed values as modified
autofillAddress() {
  const previousAddress = getAddress();
  this.form.patchValue(previousAddress, { emitEvent: false });
  this.form.markAsDirty();
}
```

**[`markAsPristine`](api/forms/FormControl#markAsPristine)** — boshqaruv elementi yoki formani pristine deb belgilaydi. Barcha bola boshqaruv elementlarini pristine deb belgilaydi va barcha ota boshqaruv elementlarining pristine holatini qayta hisoblaydi.

```ts
// Reset pristine state after saving to track new changes
saveForm() {
  this.api.save(this.form.value).subscribe(() => {
    this.form.markAsPristine();
  });
}
```

**[`markAllAsDirty`](api/forms/FormControl#markAllAsDirty)** — boshqaruv elementi yoki formani va uning barcha avlod boshqaruv elementlarini dirty deb belgilaydi.

```ts
// Mark imported data as dirty
loadData(data: FormData) {
  this.form.patchValue(data);
  this.form.markAllAsDirty();
}
```

**[`markAllAsTouched`](api/forms/FormControl#markAllAsTouched)** — boshqaruv elementi yoki formani va uning barcha avlod boshqaruv elementlarini touched deb belgilaydi. Butun forma boʻylab validatsiya xatolarini koʻrsatish uchun foydali.

```ts
// Show all validation errors before submission
onSubmit() {
  if (this.form.invalid) {
    this.form.markAllAsTouched();
    return;
  }
  this.saveForm();
}
```

## Hodisalarni chiqarish va tarqalishini boshqarish {#controlling-event-emission-and-propagation}

Forma boshqaruv elementlarini programmatik tarzda yangilashda oʻzgarishlar forma ierarxiyasi boʻylab qanday tarqalishi va hodisalar chiqarilishi yoki chiqarilmasligi ustidan aniq nazoratga egasiz.

### Hodisalarni chiqarishni tushunish {#understanding-event-emission}

Sukut boʻyicha `emitEvent: true` boʻlganda boshqaruv elementidagi har qanday oʻzgarish `valueChanges` va `statusChanges` observable'lari orqali hodisalar chiqaradi. `emitEvent: false` ni oʻrnatish bu chiqarishlarni bostiradi, bu avtomatik saqlash kabi reaktiv xatti-harakatni ishga tushirmasdan qiymatlarni programmatik tarzda oʻrnatish, boshqaruv elementlari oʻrtasidagi aylanma yangilanishlardan qochish yoki hodisalar faqat oxirida bir marta chiqarilishi kerak boʻlgan ommaviy yangilanishlarni bajarishda foydali.

```ts
@Component({/* ... */})
export class BlogPostEditor {
  postForm = new FormGroup({
    title: new FormControl(''),
    content: new FormControl(''),
  });

  constructor() {
    // Auto-save draft every time user types
    this.postForm.valueChanges.subscribe((formValue) => {
      this.autosaveDraft(formValue);
    });
  }

  loadExistingDraft(savedDraft: {title: string; content: string}) {
    // Restore draft without triggering auto-save
    this.postForm.setValue(savedDraft, {emitEvent: false});
  }
}
```

### Tarqalishni boshqarishni tushunish {#understanding-propagation-control}

Sukut boʻyicha `onlySelf: false` boʻlganda yangilanishlar ota boshqaruv elementlariga kaskad tarzda tarqalib, ularning qiymatlari va validatsiya holatini qayta hisoblaydi. `onlySelf: true` ni oʻrnatish yangilanishni joriy boshqaruv elementi bilan cheklaydi va otaga xabar berishning oldini oladi. Bu ota yangilanishini qoʻlda bir marta ishga tushirishni istagan ommaviy amallar uchun foydali.

```ts
updatePostalCodeValidator(country: string) {
  const postal = this.addressForm.get('postalCode');

  const validators = country === 'US'
    ? [Validators.maxLength(5)]
    : [Validators.maxLength(7)];

  postal.setValidators(validators);
  postal.updateValueAndValidity({ onlySelf: true, emitEvent: false });
}
```

HELPFUL: Ish vaqtida validatorlarni dinamik boshqarish haqida Forma validatsiyasi qoʻllanmasidagi [Reaktiv formalarda validatorlarni dinamik boshqarish](guide/forms/form-validation#managing-validators-dynamically-in-reactive-forms) boʻlimiga qarang.

## Forma boshqaruv elementi tiplarini toraytirish uchun yordamchi funksiyalar {#utility-functions-for-narrowing-form-control-types}

Angular `AbstractControl` ning aniq tipini aniqlashga yordam beradigan toʻrtta yordamchi funksiyani taqdim etadi. Bu funksiyalar **tip himoyachilari (type guards)** sifatida ishlaydi va `true` qaytarganda boshqaruv elementi tipini toraytiradi, bu esa xuddi shu blok ichida kichik tipga xos xususiyatlarga xavfsiz murojaat qilish imkonini beradi.

| Yordamchi funksiya | Tafsilotlar                                             |
| :--------------- | :-------------------------------------------------- |
| `isFormControl`  | Boshqaruv elementi `FormControl` boʻlganda `true` qaytaradi. |
| `isFormGroup`    | Boshqaruv elementi `FormGroup` boʻlganda `true` qaytaradi    |
| `isFormRecord`   | Boshqaruv elementi `FormRecord` boʻlganda `true` qaytaradi   |
| `isFormArray`    | Boshqaruv elementi `FormArray` boʻlganda `true` qaytaradi    |

Bu yordamchilar funksiya signaturasi `AbstractControl` qabul qiladigan, lekin mantiq muayyan boshqaruv elementi turi uchun moʻljallangan **maxsus validatorlarda** ayniqsa foydali.

```ts
import {AbstractControl, isFormArray} from '@angular/forms';

export function positiveValues(control: AbstractControl) {
  if (!isFormArray(control)) {
    return null; // Not a FormArray: validator is not applicable.
  }

  // Safe to access FormArray-specific API after narrowing.
  const hasNegative = control.controls.some((c) => c.value < 0);
  return hasNegative ? {positiveValues: true} : null;
}
```

## Reaktiv formalar API'sining qisqacha mazmuni {#reactive-forms-api-summary}

Quyidagi jadvalda reaktiv forma boshqaruv elementlarini yaratish va boshqarish uchun ishlatiladigan asosiy klasslar va servislar keltirilgan.
Toʻliq sintaksis tafsilotlari uchun [Forms paketi](api#angular_forms 'API reference') API maʼlumotnomasi hujjatlariga qarang.

### Klasslar {#classes}

| Klass             | Tafsilotlar                                                                                                                                                                                 |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AbstractControl` | Aniq forma boshqaruv elementi klasslari `FormControl`, `FormGroup` va `FormArray` uchun abstrakt asosiy klass. Ularning umumiy xatti-harakatlari va xususiyatlarini taqdim etadi.                           |
| `FormControl`     | Alohida forma boshqaruv elementining qiymati va yaroqlilik holatini boshqaradi. `<input>` yoki `<select>` kabi HTML forma boshqaruv elementiga mos keladi.                                            |
| `FormGroup`       | `AbstractControl` nusxalari guruhining qiymati va yaroqlilik holatini boshqaradi. Guruhning xususiyatlari uning bola boshqaruv elementlarini oʻz ichiga oladi. Komponentingizdagi yuqori darajadagi forma `FormGroup` hisoblanadi. |
| `FormArray`       | Raqamli indekslangan `AbstractControl` nusxalari massivining qiymati va yaroqlilik holatini boshqaradi.                                                                                     |
| `FormBuilder`     | Boshqaruv elementi nusxalarini yaratish uchun fabrika metodlarini taqdim etadigan inyeksiya qilinadigan servis.                                                                                     |
| `FormRecord`      | Har biri bir xil qiymat tipiga ega boʻlgan `FormControl` nusxalari toʻplamining qiymati va yaroqlilik holatini kuzatadi.                                                                  |

### Direktivalar {#directives}

| Direktiva              | Tafsilotlar                                                                                    |
| :--------------------- | :----------------------------------------------------------------------------------------- |
| `FormControlDirective` | Mustaqil `FormControl` nusxasini forma boshqaruv elementi bilan sinxronlaydi.                       |
| `FormControlName`      | Mavjud `FormGroup` nusxasidagi `FormControl` ni nomi boʻyicha forma boshqaruv elementi bilan sinxronlaydi. |
| `FormGroupDirective`   | Mavjud `FormGroup` nusxasini DOM elementi bilan sinxronlaydi.                                   |
| `FormGroupName`        | Ichki `FormGroup` nusxasini DOM elementi bilan sinxronlaydi.                                      |
| `FormArrayName`        | Ichki `FormArray` nusxasini DOM elementi bilan sinxronlaydi.                                      |
| `FormArrayDirective`   | Mustaqil `FormArray` nusxasini DOM elementi bilan sinxronlaydi.                                  |
