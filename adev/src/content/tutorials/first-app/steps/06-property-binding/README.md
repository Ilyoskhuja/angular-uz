# Komponent shabloniga xususiyat bogʻlash qoʻshing

Bu darslik darsi shablonga xususiyat bogʻlashni (property binding) qoʻshish va undan komponentlarga dinamik maʼlumot uzatishda foydalanishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/eM3zi_n7lNs?si=AsiczpWnMz5HhJqB&amp;start=599"/>

## Nimalarni oʻrganasiz {#what-youll-learn}

- Ilovangizning `Home` shablonida maʼlumot bogʻlashlar paydo boʻladi.
- Ilovangiz `Home` komponentidan `HousingLocation` komponentiga maʼlumot yuboradi.

## Input'larning konseptual koʻrinishi {#conceptual-preview-of-inputs}

Bu darsda ota komponentdan bola (child) komponentga maʼlumot ulashish jarayonini davom ettirasiz — buning uchun shablonda xususiyat bogʻlash yordamida oʻsha xususiyatlarga maʼlumot bogʻlaysiz.

Xususiyat bogʻlash Angular shablonida oʻzgaruvchini `Input`'ga ulash imkonini beradi. Maʼlumot soʻngra `Input`'ga dinamik tarzda bogʻlanadi.

Batafsilroq tushuntirish uchun [Xususiyat bogʻlash](/guide/templates/binding#binding-dynamic-properties-and-attributes) qoʻllanmasiga qarang.

<docs-workflow>

<docs-step title="`Home` shablonini yangilang">
Bu qadam `<app-housing-location>` tegiga xususiyat bogʻlashni qoʻshadi.

Kod muharririda:

1.  `src/app/home/home.ts` fayliga oʻting
1.  `@Component` dekoratorining template xususiyatida kodni quyidagi kodga moslab yangilang:
    <docs-code language="angular-ts" header="housingLocation xususiyat bogʻlashini qoʻshing" path="adev/src/content/tutorials/first-app/steps/07-dynamic-template-values/src/app/home/home.ts" visibleLines="[15,17]"/>

    Komponent tegiga xususiyat bogʻlashni qoʻshganda, tayinlangan qiymat satr qiymati emas, balki komponent klassidagi xususiyat sifatida qaralishi kerakligini Angular'ga bildirish uchun `[attribute] = "value"` sintaksisidan foydalanamiz.

    Oʻng tomondagi qiymat — `Home` komponentidagi xususiyatning nomi.

</docs-step>

<docs-step title="Kod hali ham ishlashini tasdiqlang">
1.  Oʻzgarishlaringizni saqlang va ilovada hech qanday xato yoʻqligini tasdiqlang.
1.  Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
</docs-step>

</docs-workflow>

SUMMARY: Bu darsda yangi xususiyat bogʻlash qoʻshdingiz va klass xususiyatiga havola uzatdingiz. Endi `HousingLocation` komponenti oʻz koʻrinishini moslashtirish uchun foydalanishi mumkin boʻlgan maʼlumotlarga ega.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="/guide/templates/binding#binding-dynamic-properties-and-attributes" title="Xususiyat bogʻlash"/>
</docs-pill-row>