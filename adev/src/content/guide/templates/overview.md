<docs-decorative-header title="Shablon sintaksisi" imgSrc="adev/src/assets/images/templates.svg"> <!-- markdownlint-disable-line -->
Angular'da shablon (template) — bu HTML boʻlagi.
Angular'ning koʻplab imkoniyatlaridan foydalanish uchun shablon ichida maxsus sintaksisdan foydalaning.
</docs-decorative-header>

TIP: Ushbu keng qamrovli qoʻllanmaga shoʻngʻishdan oldin Angular'ning [Asoslar](essentials/templates) boʻlimi bilan tanishib chiqing.

Har bir Angular komponenti komponent sahifaga render qiladigan [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)'ni belgilaydigan **shablon**ga ega. Shablonlardan foydalanish orqali Angular maʼlumotlar oʻzgarganda sahifangizni avtomatik tarzda yangilab tura oladi.

Shablonlar odatda `*.ts` faylining `template` xususiyatida yoki `*.html` faylida joylashadi. Koʻproq bilish uchun [komponentlar boʻyicha chuqur qoʻllanma](/guide/components)ga qarang.

## Shablonlar qanday ishlaydi? {#how-do-templates-work}

Shablonlar [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) sintaksisiga asoslanadi va unga oʻrnatilgan shablon funksiyalari, maʼlumotlarni bogʻlash (data binding), hodisalarni tinglash, oʻzgaruvchilar va boshqa qoʻshimcha imkoniyatlar qoʻshiladi.

Angular ilovangiz haqida ichki tasavvur hosil qilish uchun shablonlarni JavaScript'ga kompilyatsiya qiladi. Buning afzalliklaridan biri — Angular ilovangizga avtomatik tarzda qoʻllaydigan oʻrnatilgan render optimizatsiyalari.

### Standart HTML'dan farqlari {#differences-from-standard-html}

Shablonlar va standart HTML sintaksisi oʻrtasidagi baʼzi farqlar quyidagilarni oʻz ichiga oladi:

- Shablon manba kodidagi izohlar render qilingan natijaga kiritilmaydi
- Komponent va direktiva elementlari oʻz-oʻzidan yopiladigan boʻlishi mumkin (masalan, `<UserProfile />`)
- Maʼlum belgilarga ega atributlar (yaʼni `[]`, `()` va h.k.) Angular uchun alohida maʼnoga ega. Koʻproq maʼlumot uchun [bogʻlash hujjatlari](guide/templates/binding) va [hodisa tinglovchilarini qoʻshish hujjatlari](guide/templates/event-listeners)ga qarang.
- `@` belgisi Angular uchun shablonlarga [boshqaruv oqimi (control flow)](guide/templates/control-flow) kabi dinamik xatti-harakat qoʻshishda alohida maʼnoga ega. Oddiy `@` belgisini HTML entity kodi (`&commat;` yoki `&#64;`) orqali ekranlab kiritishingiz mumkin.
- Angular keraksiz boʻsh joy belgilarini eʼtiborsiz qoldiradi va qisqartiradi. Batafsil maʼlumot uchun [shablonlardagi boʻsh joylar](guide/templates/whitespace)ga qarang.
- Angular dinamik kontent uchun toʻldiruvchi (placeholder) sifatida sahifaga izoh tugunlarini qoʻshishi mumkin, lekin dasturchilar ularga eʼtibor bermasligi mumkin.

Bundan tashqari, HTML sintaksisining aksariyati toʻgʻri shablon sintaksisi hisoblansa-da, Angular shablonlarda `<script>` elementini qoʻllab-quvvatlamaydi. Koʻproq maʼlumot uchun [Xavfsizlik](best-practices/security) sahifasiga qarang.

## Keyingi qadamlar {#whats-next}

Sizni quyidagilar ham qiziqtirishi mumkin:

| Mavzular                                                                                  | Tafsilotlar                                                                                    |
| :---------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [Dinamik matn, xususiyat va atributlarni bogʻlash](guide/templates/binding)               | Dinamik maʼlumotlarni matn, xususiyat va atributlarga bogʻlang.                                |
| [Hodisa tinglovchilarini qoʻshish](guide/templates/event-listeners)                       | Shablonlaringizdagi hodisalarga javob bering.                                                  |
| [Ikki tomonlama bogʻlash](guide/templates/two-way-binding)                                | Qiymatni bogʻlash va oʻzgarishlarni tarqatishni bir vaqtda bajaradi.                           |
| [Boshqaruv oqimi](guide/templates/control-flow)                                           | Elementlarni shartli koʻrsating, yashiring va takrorlang.                                       |
| [Pipe'lar](guide/templates/pipes)                                                         | Maʼlumotlarni deklarativ tarzda oʻzgartiring.                                                  |
| [ng-content bilan bola kontentni slotlarga joylash](guide/templates/ng-content)           | Komponentlar kontentni qanday render qilishini boshqaring.                                     |
| [ng-template bilan shablon fragmentlarini yaratish](guide/templates/ng-template)          | Shablon fragmentini eʼlon qiling.                                                              |
| [ng-container bilan elementlarni guruhlash](guide/templates/ng-container)                 | Bir nechta elementni birgalikda guruhlang yoki render qilish uchun joyni belgilang.             |
| [Shablonlardagi oʻzgaruvchilar](guide/templates/variables)                                | Oʻzgaruvchilarni eʼlon qilish haqida bilib oling.                                              |
| [@defer bilan kechiktirilgan yuklash](guide/templates/defer)                              | `@defer` bilan kechiktiriladigan view'lar yarating.                                            |
| [Ifoda sintaksisi](guide/templates/expression-syntax)                                     | Angular ifodalari va standart JavaScript oʻrtasidagi oʻxshashlik va farqlarni bilib oling.     |
| [Shablonlardagi boʻsh joylar](guide/templates/whitespace)                                 | Angular boʻsh joylarni qanday qayta ishlashini bilib oling.                                    |
