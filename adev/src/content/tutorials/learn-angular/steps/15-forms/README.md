# Formalar haqida umumiy koʻrinish

Formalar koʻp ilovalarning muhim qismidir, chunki ular ilovangizga foydalanuvchi kiritmalarini qabul qilish imkonini beradi. Keling, Angular'da formalar qanday boshqarilishini oʻrganamiz.

Angular'da formalarning ikki turi bor: shablonga asoslangan (template-driven) va reaktiv (reactive). Keyingi bir necha mashgʻulotda ikkalasini ham oʻrganasiz.

NOTE: [Chuqur qoʻllanmada Angular'dagi formalar](/guide/forms) haqida koʻproq bilib oling.

Bu mashgʻulotda shablonga asoslangan yondashuv yordamida formani qanday sozlashni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="Kiritish maydonini yarating">

`user.ts` faylida shablonni `id` qiymati `framework`, turi `text` boʻlgan matn kiritish maydonini qoʻshish orqali yangilang.

```angular-html
<label for="framework">
  Favorite Framework:
  <input id="framework" type="text" />
</label>
```

</docs-step>

<docs-step title="`FormsModule`'ni import qiling">

Bu forma formalarga maʼlumotlarni bogʻlash imkonini beruvchi Angular xususiyatlaridan foydalanishi uchun `FormsModule`'ni import qilishingiz kerak boʻladi.

`@angular/forms`'dan `FormsModule`'ni import qiling va uni `User` komponentining `imports` massiviga qoʻshing.

```ts {highlight:[[2],[6]]}
import {Component} from '@angular/core';
import {FormsModule} from '@angular/forms';

@Component({
...
imports: [FormsModule],
})
export class User {}
```

</docs-step>

<docs-step title="Input qiymatiga bogʻlash qoʻshing">

`FormsModule`'da `ngModel` deb nomlangan direktiva bor, u input qiymatini klassingizdagi xususiyatga bogʻlaydi.

Inputni `ngModel` direktivasidan foydalanishga yangilang, xususan `favoriteFramework` xususiyatiga bogʻlash uchun quyidagi sintaksisdan foydalaning: `[(ngModel)]="favoriteFramework"`.

```html {highlight:[3]}
<label for="framework">
  Favorite Framework:
  <input id="framework" type="text" [(ngModel)]="favoriteFramework" />
</label>
```

Oʻzgarishlarni kiritganingizdan soʻng, kiritish maydoniga qiymat kiritib koʻring. Uning ekranda qanday yangilanishiga eʼtibor bering (ha, juda zoʻr).

NOTE: `[()]` sintaksisi "qutidagi banan" (banana in a box) deb ataladi, lekin u ikki tomonlama bogʻlashni ifodalaydi: xususiyat bogʻlash va hodisa bogʻlash. [Ikki tomonlama maʼlumot bogʻlash haqidagi Angular hujjatlarida](guide/templates/two-way-binding) koʻproq bilib oling.

</docs-step>

</docs-workflow>

Endi Angular bilan formalar yaratish yoʻlida muhim birinchi qadamni tashladingiz.

Ajoyib ish. Shu zaylda davom etaylik!
