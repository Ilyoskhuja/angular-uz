# Rasmlarni optimallashtirish

Rasmlar koʻplab ilovalarning katta qismini tashkil qiladi va past [Core Web Vitals](https://web.dev/explore/learn-core-web-vitals) ballari kabi ilova unumdorligi muammolarining asosiy sababchisi boʻlishi mumkin.

Rasmlarni optimallashtirish murakkab mavzu boʻlishi mumkin, lekin Angular `NgOptimizedImage` direktivasi yordamida buning koʻp qismini siz uchun bajaradi.

NOTE: [Chuqur qoʻllanmada NgOptimizedImage bilan rasmlarni optimallashtirish](/guide/image-optimization) haqida koʻproq bilib oling.

Bu mashgʻulotda rasmlaringiz samarali yuklanishini taʼminlash uchun `NgOptimizedImage`'dan qanday foydalanishni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="NgOptimizedImage direktivasini import qiling">

`NgOptimizedImage` direktivasidan foydalanish uchun avval uni `@angular/common` kutubxonasidan import qiling va komponentning `imports` massiviga qoʻshing.

```ts
import { NgOptimizedImage } from '@angular/common';

@Component({
  imports: [NgOptimizedImage],
  ...
})
```

</docs-step>

<docs-step title="src atributini ngSrc'ga oʻzgartiring">

`NgOptimizedImage` direktivasini yoqish uchun `src` atributini `ngSrc`'ga almashtiring. Bu statik rasm manbalariga (yaʼni `src`) ham, dinamik rasm manbalariga (yaʼni `[src]`) ham tegishli.

```angular-ts {highlight:[[7],[11]]}
import { NgOptimizedImage } from '@angular/common';

@Component({
template: `     ...
    <li>
      Static Image:
      <img ngSrc="/logo.svg" alt="Angular logo" width="32" height="32" />
    </li>
    <li>
      Dynamic Image:
      <img [ngSrc]="logoUrl" [alt]="logoAlt" width="32" height="32" />
    </li>
    ...
  `,
imports: [NgOptimizedImage],
})
```

</docs-step>

<docs-step title="width va height atributlarini qoʻshing">

Yuqoridagi kod misolida har bir rasmda `width` va `height` atributlarining ikkalasi ham borligiga eʼtibor bering. [Layout shift](https://web.dev/articles/cls) yuz berishining oldini olish uchun `NgOptimizedImage` direktivasi har bir rasmda ikkala oʻlcham atributini talab qiladi.

Rasmlar uchun statik `height` va `width` koʻrsata olmaydigan yoki koʻrsatishni istamaydigan holatlarda rasmga oʻzini oʻz ichiga olgan elementni toʻldiradigan "fon rasmi" kabi tutishini aytish uchun [`fill` atributidan](/guide/image-optimization#using-fill-mode) foydalanishingiz mumkin:

```angular-html
// Container div has 'position: "relative"'
<div class="image-container">
  <img ngSrc="www.example.com/image.png" fill />
</div>
```

NOTE: `fill` rasmi toʻgʻri render qilinishi uchun uning ota elementi `position: "relative"`, `position: "fixed"` yoki `position: "absolute"` stiliga ega boʻlishi kerak.

</docs-step>

<docs-step title="Muhim rasmlarga ustuvorlik bering">

Yuklash unumdorligi uchun eng muhim optimallashtirishlardan biri — ["LCP element"](https://web.dev/articles/optimize-lcp) boʻlishi mumkin boʻlgan har qanday rasmga ustuvorlik berish; LCP element — sahifa yuklanganda ekrandagi eng katta grafik element. Yuklash vaqtlarini optimallashtirish uchun "hero image"ingizga yoki LCP element boʻlishi mumkin deb hisoblagan boshqa rasmlarga `priority` atributini qoʻshishni unutmang.

```ts
<img ngSrc="www.example.com/image.png" height="600" width="800" priority />
```

</docs-step>

<docs-step title="Ixtiyoriy: rasm yuklovchisidan (image loader) foydalaning">

`NgOptimizedImage` [rasm yuklovchisini](guide/image-optimization#configuring-an-image-loader-for-ngoptimizedimage) koʻrsatish imkonini beradi; u direktivaga rasmlaringiz uchun URL'larni qanday formatlashni aytadi. Yuklovchidan foydalanish rasmlaringizni qisqa, nisbiy URL'lar bilan aniqlash imkonini beradi:

```ts
providers: [provideImgixLoader('https://my.base.url/')],
```

Yakuniy URL 'https://my.base.url/image.png' boʻladi

```angular-html
<img ngSrc="image.png" height="600" width="800" />
```

Rasm yuklovchilari shunchaki qulaylik uchun emas — ular `NgOptimizedImage`'ning toʻliq imkoniyatlaridan foydalanish imkonini beradi. Bu optimallashtirishlar va mashhur CDN'lar uchun oʻrnatilgan yuklovchilar haqida koʻproq [bu yerda](guide/image-optimization#configuring-an-image-loader-for-ngoptimizedimage) bilib oling.

</docs-step>

</docs-workflow>

Bu direktivani ish jarayoningizga qoʻshish orqali rasmlaringiz endi Angular yordamida eng yaxshi amaliyotlar asosida yuklanadi 🎉

Koʻproq bilmoqchi boʻlsangiz, [`NgOptimizedImage` hujjatlariga](guide/image-optimization) qarang. Ajoyib ishni davom ettiring, keyin marshrutlash haqida oʻrganamiz.
