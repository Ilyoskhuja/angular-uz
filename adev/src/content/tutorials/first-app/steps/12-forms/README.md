# Angular ilovangizga forma qoʻshish

Bu dars Angular ilovasiga foydalanuvchi maʼlumotlarini yigʻuvchi formani qanday qoʻshishni koʻrsatadi.
Bu dars ishlaydigan Angular ilovasidan boshlanadi va unga formani qanday qoʻshishni koʻrsatadi.

Forma yigʻadigan maʼlumotlar faqat ilova servisiga yuboriladi, u esa ularni brauzer konsoliga yozadi.
Forma maʼlumotlarini yuborish va qabul qilish uchun REST API'dan foydalanish bu darsda yoritilmaydi.

<docs-video src="https://www.youtube.com/embed/kWbk-dOJaNQ?si=FYMXGdUiT-qh321h"/>

IMPORTANT: Darslikning bu qadami uchun lokal muhitingizdan foydalanishni tavsiya qilamiz.

## Nimalarni oʻrganasiz {#what-youll-learn}

- Ilovangizda foydalanuvchilar maʼlumot kirita oladigan forma boʻladi va bu maʼlumotlar ilova servisiga yuboriladi.
- Servis formadagi maʼlumotlarni brauzer konsoli jurnaliga (console log) yozadi.

<docs-workflow>

<docs-step title="Forma maʼlumotlarini yuborish uchun metod qoʻshing {#add-a-method-to-send-form-data}">
Bu qadam ilovangiz servisiga forma maʼlumotlarini qabul qilib, ularni maʼlumotlar manziliga yuboradigan metod qoʻshadi.
Bu misolda metod formadagi maʼlumotlarni brauzer konsoli jurnaliga yozadi.

IDE'ingizning **Edit** panelida:

1.  `src/app/housing.service.ts` faylida, `HousingService` klassi ichida, klass taʼrifining oxiriga quyidagi metodni joylashtiring.

       <docs-code header="src/app/housing.service.ts dagi submit metodi" path="adev/src/content/tutorials/first-app/steps/13-search/src/app/housing.service.ts" visibleLines="[118,122]"/>

1.  Ilova xatosiz build boʻlishini tasdiqlang.
    Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
    </docs-step>

<docs-step title="Tafsilotlar sahifasiga forma funksiyalarini qoʻshing {#add-the-form-functions-to-the-details-page}">
Bu qadam tafsilotlar sahifasiga forma bilan oʻzaro aloqalarni boshqaradigan kodni qoʻshadi.

IDE'ingizning **Edit** panelida, `src/app/details/details.ts` faylida:

1.  Fayl boshidagi `import` ifodalaridan keyin Angular forma klasslarini import qilish uchun quyidagi kodni qoʻshing.

      <docs-code header="src/app/details/details.ts dagi forma importlari" path="adev/src/content/tutorials/first-app/steps/13-search/src/app/details/details.ts" visibleLines="[5]"/>

1.  `Details` dekoratori metadatasida `imports` xususiyatini quyidagi kod bilan yangilang:

      <docs-code header="src/app/details/details.ts dagi imports direktivasi" path="adev/src/content/tutorials/first-app/steps/13-search/src/app/details/details.ts" visibleLines="[9]"/>

1.  `Details` klassida, `constructor()` metodidan oldin, forma obyektini yaratish uchun quyidagi kodni qoʻshing.

      <docs-code header="src/app/details/details.ts dagi template direktivasi" path="adev/src/content/tutorials/first-app/steps/13-search/src/app/details/details.ts" visibleLines="[52,56]"/>

    Angular'da `FormGroup` va `FormControl` — formalar yaratish imkonini beruvchi turlar. `FormControl` turi sukut boʻyicha qiymat berishi va forma maʼlumotlarini shakllantirishi mumkin. Bu misolda `firstName` — `string` va sukut boʻyicha qiymati boʻsh satr.

1.  `Details` klassida, `constructor()` metodidan keyin, **Apply now** bosilishiga ishlov berish uchun quyidagi kodni qoʻshing.

      <docs-code header="src/app/details/details.ts dagi template direktivasi" path="adev/src/content/tutorials/first-app/steps/13-search/src/app/details/details.ts" visibleLines="[62,68]"/>

    Bu tugma hali mavjud emas — uni keyingi qadamda qoʻshasiz. Yuqoridagi kodda `FormControl`'lar `null` qaytarishi mumkin. Bu kod qiymat `null` boʻlsa, sukut boʻyicha boʻsh satrni ishlatish uchun nullish coalescing operatoridan foydalanadi.

1.  Ilova xatosiz build boʻlishini tasdiqlang.
    Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
    </docs-step>

<docs-step title="Tafsilotlar sahifasiga forma markup'ini qoʻshing {#add-the-forms-markup-to-the-details-page}">
Bu qadam tafsilotlar sahifasiga formani koʻrsatadigan markup'ni qoʻshadi.

IDE'ingizning **Edit** panelida, `src/app/details/details.ts` faylida:

1. `Details` dekoratori metadatasida forma markup'ini qoʻshish uchun `template` HTML'ini quyidagi kodga moslab yangilang.

   <docs-code language="angular-ts" header="src/app/details/details.ts dagi template direktivasi" path="adev/src/content/tutorials/first-app/steps/13-search/src/app/details/details.ts" visibleLines="[10,45]"/>

   Endi shablon `(submit)="submitApplication()"` hodisa ishlov beruvchisini oʻz ichiga oladi. Angular shablon kodida hodisalarni aniqlash uchun hodisa nomi atrofida qavs sintaksisidan foydalanadi. Tenglik belgisining oʻng tomonidagi kod — bu hodisa ishga tushganda bajarilishi kerak boʻlgan kod. Siz brauzer hodisalariga ham, maxsus (custom) hodisalarga ham bogʻlanishingiz mumkin.

1. Ilova xatosiz build boʻlishini tasdiqlang.
   Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.

   <img alt="details page with a form for applying to live at this location" src="assets/images/tutorials/first-app/homes-app-lesson-12-step-3.png">

</docs-step>

<docs-step title="Ilovangizning yangi formasini sinab koʻring {#test-your-apps-new-form}">
Bu qadam yangi formani sinab, forma maʼlumotlari ilovaga yuborilganda ular konsol jurnalida paydo boʻlishini tekshiradi.

1. IDE'ingizning **Terminal** panelida, agar hali ishlamayotgan boʻlsa, `ng serve`'ni ishga tushiring.
1. Brauzeringizda ilovangizni `http://localhost:4200` manzilida oching.
1. Brauzerda ilova ustida sichqonchaning oʻng tugmasini bosing va kontekst menyusidan **Inspect** bandini tanlang.
1. Dasturchi asboblari oynasida **Console** yorligʻini tanlang.
   Keyingi qadamlar uchun dasturchi asboblari oynasi koʻrinib turishiga ishonch hosil qiling
1. Ilovangizda:
   1. Turar joyni tanlang va uy haqidagi tafsilotlarni koʻrish uchun **Learn more** tugmasini bosing.
   1. Uyning tafsilotlar sahifasida yangi formani topish uchun eng pastga oʻting.
   1. Forma maydonlariga maʼlumot kiriting — istalgan maʼlumot boʻlishi mumkin.
   1. Maʼlumotlarni yuborish uchun **Apply now** tugmasini tanlang.
1. Dasturchi asboblari oynasida forma maʼlumotlaringizni topish uchun jurnal chiqishini koʻrib chiqing.
   </docs-step>

</docs-workflow>

SUMMARY: Bu darsda siz ilovangizni Angular'ning formalar imkoniyatidan foydalanib forma qoʻshadigan qilib yangiladingiz va formada olingan maʼlumotlarni hodisa ishlov beruvchisi orqali komponentga uladingiz.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/forms" title="Angular formalari"/>
  <docs-pill href="guide/templates/event-listeners" title="Hodisalarga ishlov berish"/>
</docs-pill-row>
