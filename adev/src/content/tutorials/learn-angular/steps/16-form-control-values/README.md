# Forma boshqaruv elementi qiymatini olish

Formalaringiz Angular bilan sozlanganidan soʻng, keyingi qadam — forma boshqaruv elementlaridan (form control) qiymatlarni olish.

NOTE: [Chuqur qoʻllanmada asosiy forma boshqaruv elementini qoʻshish](/guide/forms/reactive-forms#adding-a-basic-form-control) haqida koʻproq bilib oling.

Bu mashgʻulotda forma inputingizdan qiymatni qanday olishni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="Kiritish maydonining qiymatini shablonda koʻrsating">

Input qiymatini shablonda koʻrsatish uchun komponentning boshqa har qanday klass xususiyati kabi `{{}}` interpolyatsiya sintaksisidan foydalanishingiz mumkin:

```angular-ts {highlight:[5]}
@Component({
  selector: 'app-user',
  template: `
    ...
    <p>Framework: {{ favoriteFramework }}</p>
    <label for="framework">
      Favorite Framework:
      <input id="framework" type="text" [(ngModel)]="favoriteFramework" />
    </label>
  `,
})
export class User {
  favoriteFramework = '';
}
```

</docs-step>

<docs-step title="Kiritish maydonining qiymatini oling">

Komponent klassida kiritish maydoni qiymatiga murojaat qilish kerak boʻlganda, buni `this` sintaksisi orqali klass xususiyatiga murojaat qilish yoʻli bilan amalga oshirishingiz mumkin.

```angular-ts {highlight:[15]}
...
@Component({
  selector: 'app-user',
  template: `
    ...
    <button (click)="showFramework()">Show Framework</button>
  `,
  ...
})
export class User {
  favoriteFramework = '';
  ...

  showFramework() {
    alert(this.favoriteFramework);
  }
}
```

</docs-step>

</docs-workflow>

Input qiymatlarini shablonda koʻrsatish va ularga programmali tarzda murojaat qilishni oʻrganganingiz uchun ajoyib ish.

Endi Angular bilan formalarni boshqarishning keyingi usuliga — reaktiv formalarga oʻtish vaqti keldi. Shablonga asoslangan formalar haqida koʻproq bilmoqchi boʻlsangiz, [Angular formalar hujjatlariga](guide/forms/template-driven-forms) qarang.
