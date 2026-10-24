# Birinchi Angular ilovangizni yarating

Bu darslik Angular'da kod yozishni boshlash uchun bilishingiz kerak boʻlgan Angular tushunchalari bilan tanishtiruvchi darslardan iborat.

Ularni xohlaganingizcha koʻp yoki kam bajarishingiz va istalgan tartibda oʻtishingiz mumkin.

HELPFUL: Videoni afzal koʻrasizmi? Bu darslik uchun toʻliq [YouTube kursimiz](https://youtube.com/playlist?list=PL1w1q3fL4pmj9k1FrJ3Pe91EPub2_h4jF&si=1q9889ulHp8VZ0e7) ham bor!

<docs-video src="https://www.youtube.com/embed/xAT0lHYhHMY?si=cKUW_MGn3MesFT7o"/>

## Boshlashdan oldin {#before-you-start}

Bu darslikdan eng yaxshi natija olish uchun quyidagi talablarni koʻrib chiqing va muvaffaqiyatga erishish uchun kerakli hamma narsa sizda mavjudligiga ishonch hosil qiling.

### Sizning tajribangiz {#your-experience}

Bu darslikdagi darslar sizda quyidagi tajriba borligini nazarda tutadi:

1. HTML'ni bevosita tahrirlab HTML veb-sahifa yaratgansiz.
1. JavaScript'da veb-sayt kontentini dasturlagansiz.
1. Cascading Style Sheet (CSS) kontentini oʻqib, selektorlar qanday ishlatilishini tushunasiz.
1. Kompyuteringizda vazifalarni bajarish uchun buyruq qatori koʻrsatmalaridan foydalangansiz.

### Sizning jihozlaringiz {#your-equipment}

Bu darslarni Angular vositalarining lokal oʻrnatmasi yordamida yoki bizning oʻrnatilgan (embedded) muharririmizda bajarish mumkin. Lokal Angular dasturlashni Windows, macOS yoki Linux asosidagi tizimlarda amalga oshirish mumkin.

NOTE: Shunga oʻxshash ogohlantirishlarga eʼtibor bering — ular faqat lokal muharriringiz uchun moʻljallangan boʻlishi mumkin boʻlgan qadamlarni ajratib koʻrsatadi.

## Birinchi Angular ilovangizning konseptual koʻrinishi {#conceptual-preview-of-your-first-angular-app}

Bu darslikdagi darslar ijaraga beriladigan uylar roʻyxatini chiqaruvchi va alohida uylarning tafsilotlarini koʻrsatuvchi Angular ilovasini yaratadi.
Bu ilova koʻplab Angular ilovalariga xos boʻlgan imkoniyatlardan foydalanadi.

<img alt="Output of homes landing page" src="assets/images/tutorials/first-app/homes-app-landing-page.png">

## Lokal dasturlash muhiti {#local-development-environment}

NOTE: Bu qadam faqat lokal muhitingiz uchun!

Bu qadamlarni ushbu darslik uchun ishlatmoqchi boʻlgan kompyuteringizdagi buyruq qatori vositasida bajaring.

<docs-workflow>

<docs-step title="Angular talab qiladigan `node.js` versiyasini aniqlang {#identify-the-version-of-nodejs-that-angular-requires}">
Angular Node'ning faol LTS yoki texnik xizmat koʻrsatiladigan (maintenance) LTS versiyasini talab qiladi. Keling, `node.js` versiyangizni tekshiramiz. Muayyan versiya talablari haqida maʼlumot olish uchun [package.json faylidagi](https://unpkg.com/browse/@angular/core@15.1.5/package.json) engines xususiyatiga qarang.

**Terminal** oynasida:

1. Quyidagi buyruqni bajaring: `node --version`
1. Koʻrsatilgan versiya raqami talablarga javob berishini tasdiqlang.
   </docs-step>

<docs-step title="Angular uchun `node.js`'ning toʻgʻri versiyasini oʻrnating {#install-the-correct-version-of-nodejs-for-angular}">
Agar sizda `node.js` versiyasi oʻrnatilmagan boʻlsa, [nodejs.org'dagi oʻrnatish koʻrsatmalariga](https://nodejs.org/en/download/) amal qiling
</docs-step>

<docs-step title="Angular'ning soʻnggi versiyasini oʻrnating {#install-the-latest-version-of-angular}">
`node.js` va `npm` oʻrnatilgach, keyingi qadam — samarali Angular dasturlash uchun vositalar taqdim etuvchi [Angular CLI](tools/cli)'ni oʻrnatish.

**Terminal** oynasida quyidagi buyruqni bajaring: `npm install -g @angular/cli`.
</docs-step>

<docs-step title="Integratsiyalashgan dasturlash muhitini (IDE) oʻrnating {#install-integrated-development-environment-ide}">
Angular bilan ilova yaratish uchun oʻzingizga qulay istalgan vositadan foydalanishingiz mumkin. Biz quyidagilarni tavsiya qilamiz:

1. [Visual Studio Code](https://code.visualstudio.com/)
2. Ixtiyoriy, lekin tavsiya etiladigan qadam sifatida [Angular Language Service](https://marketplace.visualstudio.com/items?itemName=Angular.ng-template)'ni oʻrnatib, dasturchi tajribangizni yanada yaxshilashingiz mumkin
3. [WebStorm](https://www.jetbrains.com/webstorm/)
   </docs-step>

<docs-step title="Ixtiyoriy: AI yordamchili IDE'ingizni sozlang {#optional-set-up-your-ai-powered-ide}">

Agar bu darslikni oʻzingiz afzal koʻrgan AI yordamchili IDE'da oʻtayotgan boʻlsangiz, [Angular prompt qoidalari va eng yaxshi amaliyotlari bilan tanishing](/ai/develop-with-ai).

</docs-step>

</docs-workflow>

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="/overview" title="Angular nima"/>
  <docs-pill href="/tools/cli/setup-local" title="Lokal muhit va ish maydonini sozlash"/>
  <docs-pill href="/cli" title="Angular CLI maʼlumotnomasi"/>
</docs-pill-row>
