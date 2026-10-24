# Navigatsiya uchun RouterLink'dan foydalanish

Ilovaning hozirgi holatida ilova ichidagi ichki havolani bosganimizda butun sahifa yangilanadi. Kichik ilovada bu unchalik sezilmasligi mumkin, lekin kontenti koʻproq boʻlgan kattaroq sahifalarda bu unumdorlikka taʼsir qilishi mumkin, chunki foydalanuvchilar resurslarni qayta yuklab olishi va hisob-kitoblarni qaytadan bajarishi kerak boʻladi.

NOTE: [Chuqur qoʻllanmada ilovangizga marshrutlar qoʻshish](/guide/routing/define-routes#adding-the-router-to-your-application) haqida koʻproq bilib oling.

Bu mashgʻulotda Angular Router'dan toʻliq foydalanish uchun `RouterLink` direktivasini qanday ishlatishni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="`RouterLink` direktivasini import qiling {#import-routerlink-directive}">

`app.ts` faylida `@angular/router`'dan mavjud import ifodasiga `RouterLink` direktivasi importini qoʻshing va uni komponent dekoratoringizning `imports` massiviga qoʻshing.

```ts
...
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  imports: [RouterLink, RouterOutlet],
  ...
})
```

</docs-step>

<docs-step title="Shablonga `routerLink` qoʻshing {#add-a-routerlink-to-template}">

`RouterLink` direktivasidan foydalanish uchun `href` atributlarini `routerLink` bilan almashtiring. Shablonni shu oʻzgarish bilan yangilang.

```angular-ts
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  ...
  template: `
    ...
    <a routerLink="/">Home</a>
    <a routerLink="/user">User</a>
    ...
  `,
  imports: [RouterLink, RouterOutlet],
})
```

</docs-step>

</docs-workflow>

Endi navigatsiyadagi havolalarni bosganingizda hech qanday miltillashni koʻrmasligingiz va faqat sahifaning oʻzi kontenti (yaʼni `router-outlet`) oʻzgarishini koʻrishingiz kerak 🎉

Angular bilan marshrutlashni oʻrganganingiz uchun ajoyib ish. Bu `Router` API'ning faqat yuzaki qismi; koʻproq bilish uchun [Angular Router hujjatlariga](guide/routing) qarang.
