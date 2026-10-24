# Kechiktiriladigan view'lar

Baʼzan ilova yaratishda ilovangizda murojaat qilish kerak boʻlgan juda koʻp komponentlar paydo boʻladi, lekin ulardan baʼzilarini turli sabablarga koʻra darhol yuklash shart emas.

Ehtimol ular koʻrinadigan qismdan pastda joylashgan yoki keyinroqgacha ular bilan oʻzaro taʼsir qilinmaydigan ogʻir komponentlardir. Bunday holda biz bu resurslarning baʼzilarini kechiktiriladigan view'lar yordamida keyinroq yuklashimiz mumkin.

NOTE: [Chuqur qoʻllanmada @defer bilan kechiktirilgan yuklash](/guide/templates/defer) haqida koʻproq bilib oling.

Bu mashgʻulotda komponent shabloningizning bir boʻlimini kechiktirib yuklash uchun kechiktiriladigan view'lardan qanday foydalanishni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="Izohlar komponenti atrofiga `@defer` bloki qoʻshing">

Ilovangizda blog posti sahifasida post tafsilotlaridan keyin izohlar komponenti bor.

Izohlar komponentini kechiktirib yuklash uchun uni `@defer` bloki bilan oʻrang.

```angular-html
@defer {
  <comments />
}
```

Yuqoridagi kod oddiy `@defer` blokidan qanday foydalanishga misol. Sukut boʻyicha `@defer` `comments` komponentini brauzer boʻsh (idle) boʻlganda yuklaydi.

</docs-step>

<docs-step title="Toʻldiruvchi (placeholder) qoʻshing">

`@defer` blokiga `@placeholder` bloki qoʻshing. `@placeholder` bloki — kechiktirilgan yuklash boshlanishidan oldin koʻrsatiladigan html joylashtiriladigan joy. `@placeholder` bloklaridagi kontent darhol (eager) yuklanadi.

```angular-html {highlight:[3,4,5]}
@defer {
  <comments />
} @placeholder {
  <p>Future comments</p>
}
```

</docs-step>

<docs-step title="Yuklanish bloki qoʻshing">

`@defer` blokiga `@loading` bloki qoʻshing. `@loading` bloki — kechiktirilgan kontent faol tarzda yuklab olinayotgan, lekin hali tugallanmagan _vaqtda_ koʻrsatiladigan html joylashtiriladigan joy. `@loading` bloklaridagi kontent darhol yuklanadi.

```angular-html {highlight:[5,6,7]}
@defer {
  <comments />
} @placeholder {
  <p>Future comments</p>
} @loading {
  <p>Loading comments...</p>
}
```

</docs-step>

<docs-step title="Minimal davomiylik qoʻshing">

`@placeholder` va `@loading` boʻlimlarining ikkalasida ham yuklash tez sodir boʻlganda miltillashning oldini olish uchun ixtiyoriy parametrlar mavjud. `@placeholder`'da `minimum`, `@loading`'da esa `minimum` va `after` bor. `@loading` blokiga kamida 2 soniya davomida render qilinishi uchun `minimum` davomiylikni qoʻshing.

```angular-html {highlight:[5]}
@defer {
  <comments />
} @placeholder {
  <p>Future comments</p>
} @loading (minimum 2s) {
  <p>Loading comments...</p>
}
```

</docs-step>

<docs-step title="Viewport triggeri qoʻshing">

Kechiktiriladigan view'larda bir qancha trigger variantlari mavjud. Kontent viewport'ga kirganda kechiktirib yuklanishi uchun viewport triggerini qoʻshing.

```angular-html {highlight:[1]}
@defer (on viewport) {
  <comments />
} @placeholder {
  <p>Future comments</p>
} @loading (minimum 2s) {
  <p>Loading comments...</p>
}
```

</docs-step>

<docs-step title="Kontent qoʻshing">

Viewport triggeridan koʻrish uchun sahifani aylantirish (scroll) kerak boʻladigan darajada pastda joylashgan kontentni kechiktirayotganingizda foydalanish eng maqsadga muvofiq. Shuning uchun blog postimizga biroz kontent qoʻshamiz. Oʻzingiz yozishingiz yoki quyidagi kontentni nusxalab, `<article>` elementi ichiga joylashtirishingiz mumkin.

```html {highlight:[1]}
<article>
  <p>
    Angular is my favorite framework, and this is why. Angular has the coolest deferrable view
    feature that makes defer loading content the easiest and most ergonomic it could possibly be.
    The Angular community is also filled with amazing contributors and experts that create excellent
    content. The community is welcoming and friendly, and it really is the best community out there.
  </p>
  <p>
    I can't express enough how much I enjoy working with Angular. It offers the best developer
    experience I've ever had. I love that the Angular team puts their developers first and takes
    care to make us very happy. They genuinely want Angular to be the best framework it can be, and
    they're doing such an amazing job at it, too. This statement comes from my heart and is not at
    all copied and pasted. In fact, I think I'll say these exact same things again a few times.
  </p>
  <p>
    Angular is my favorite framework, and this is why. Angular has the coolest deferrable view
    feature that makes defer loading content the easiest and most ergonomic it could possibly be.
    The Angular community is also filled with amazing contributors and experts that create excellent
    content. The community is welcoming and friendly, and it really is the best community out there.
  </p>
  <p>
    I can't express enough how much I enjoy working with Angular. It offers the best developer
    experience I've ever had. I love that the Angular team puts their developers first and takes
    care to make us very happy. They genuinely want Angular to be the best framework it can be, and
    they're doing such an amazing job at it, too. This statement comes from my heart and is not at
    all copied and pasted. In fact, I think I'll say these exact same things again a few times.
  </p>
  <p>
    Angular is my favorite framework, and this is why. Angular has the coolest deferrable view
    feature that makes defer loading content the easiest and most ergonomic it could possibly be.
    The Angular community is also filled with amazing contributors and experts that create excellent
    content. The community is welcoming and friendly, and it really is the best community out there.
  </p>
  <p>
    I can't express enough how much I enjoy working with Angular. It offers the best developer
    experience I've ever had. I love that the Angular team puts their developers first and takes
    care to make us very happy. They genuinely want Angular to be the best framework it can be, and
    they're doing such an amazing job at it, too. This statement comes from my heart and is not at
    all copied and pasted.
  </p>
</article>
```

Bu kodni qoʻshganingizdan soʻng, pastga aylantiring va kechiktirilgan kontent viewport'ga kirganda yuklanishini koʻring.

</docs-step>

</docs-workflow>

Bu mashgʻulotda ilovalaringizda kechiktiriladigan view'lardan qanday foydalanishni oʻrgandingiz. Ajoyib ish. 🙌

Ular bilan yana koʻproq ishlar qilish mumkin, masalan, turli triggerlar, oldindan yuklash (prefetching) va `@error` bloklari.

Koʻproq bilmoqchi boʻlsangiz, [Kechiktiriladigan view'lar hujjatlariga](/guide/templates/defer) qarang.
