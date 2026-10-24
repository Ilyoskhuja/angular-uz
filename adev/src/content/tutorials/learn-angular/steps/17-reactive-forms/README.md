# Reaktiv formalar

Formalaringizni faqat shablonga tayanish oʻrniga programmali tarzda boshqarmoqchi boʻlsangiz, reaktiv formalar — bunga javob.

NOTE: [Chuqur qoʻllanmada reaktiv formalar](/guide/forms/reactive-forms) haqida koʻproq bilib oling.

Bu mashgʻulotda reaktiv formalarni qanday sozlashni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="`ReactiveForms` modulini import qiling {#import-reactiveforms-module}">

`app.ts` faylida `@angular/forms`'dan `ReactiveFormsModule`'ni import qiling va uni komponentning `imports` massiviga qoʻshing.

```angular-ts
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  template: `
    <form>
      <label>Name
        <input type="text" />
      </label>
      <label>Email
        <input type="email" />
      </label>
      <button type="submit">Submit</button>
    </form>
  `,
  imports: [ReactiveFormsModule],
})
```

</docs-step>

<docs-step title="FormControl'lar bilan `FormGroup` obyektini yarating {#create-the-formgroup-object-with-formcontrols}">

Reaktiv formalar forma boshqaruv elementlarini (masalan, inputlarni) ifodalash uchun `FormControl` klassidan foydalanadi. Angular forma boshqaruv elementlarini foydali obyektga guruhlash uchun `FormGroup` klassini taqdim etadi, bu katta formalar bilan ishlashni dasturchilar uchun qulayroq qiladi.

`@angular/forms`'dan importga `FormControl` va `FormGroup`'ni qoʻshing, shunda har bir forma uchun `name` va `email` xususiyatlari FormControl boʻlgan FormGroup yaratishingiz mumkin.

```ts
import {ReactiveFormsModule, FormControl, FormGroup } from '@angular/forms';
...
export class App {
  profileForm = new FormGroup({
    name: new FormControl(''),
    email: new FormControl(''),
  });
}
```

</docs-step>

<docs-step title="FormGroup va FormControl'larni formaga bogʻlang {#link-the-formgroup-and-formcontrols-to-the-form}">

Har bir `FormGroup` `[formGroup]` direktivasi yordamida formaga biriktirilishi kerak.

Bundan tashqari, har bir `FormControl` `formControlName` direktivasi bilan biriktirilib, tegishli xususiyatga tayinlanishi mumkin. Shablonni quyidagi forma kodi bilan yangilang:

```angular-html
<form [formGroup]="profileForm">
  <label>
    Name
    <input type="text" formControlName="name" />
  </label>
  <label>
    Email
    <input type="email" formControlName="email" />
  </label>
  <button type="submit">Submit</button>
</form>
```

</docs-step>

<docs-step title="Forma yangilanishini qayta ishlang {#handle-update-to-the-form}">

`FormGroup`'dan maʼlumotlarga murojaat qilmoqchi boʻlsangiz, buni `FormGroup`'ning qiymatiga murojaat qilish orqali amalga oshirish mumkin. Forma qiymatlarini koʻrsatish uchun `template`'ni yangilang:

```angular-html
...
<h2>Profile Form</h2>
<p>Name: {{ profileForm.value.name }}</p>
<p>Email: {{ profileForm.value.email }}</p>
```

</docs-step>

<docs-step title="FormGroup qiymatlariga murojaat qiling {#access-formgroup-values}">
Komponent klassiga `handleSubmit` deb nomlangan yangi metod qoʻshing, uni keyinroq forma yuborilishini qayta ishlash uchun ishlatasiz.
Bu metod formadagi qiymatlarni koʻrsatadi, qiymatlarga FormGroup orqali murojaat qilishingiz mumkin.

Komponent klassida forma yuborilishini qayta ishlash uchun `handleSubmit()` metodini qoʻshing.

```ts
handleSubmit() {
  alert(
    this.profileForm.value.name + ' | ' + this.profileForm.value.email
  );
}
```

</docs-step>

<docs-step title="Formaga `ngSubmit` qoʻshing {#add-ngsubmit-to-the-form}">
Forma qiymatlariga murojaat qila olasiz, endi yuborish hodisasini qayta ishlash va `handleSubmit` metodidan foydalanish vaqti keldi.
Angular'da aynan shu maqsad uchun `ngSubmit` deb nomlangan hodisa ishlov beruvchisi mavjud. Forma yuborilganda `handleSubmit` metodini chaqirish uchun forma elementini yangilang.

```angular-html {highlight:[1]}
<form [formGroup]="profileForm" (ngSubmit)="handleSubmit()"></form>
```

</docs-step>

</docs-workflow>

Va shu tarzda, endi Angular'da reaktiv formalar bilan qanday ishlashni bilasiz.

Bu mashgʻulotni ajoyib bajardingiz. Forma validatsiyasi haqida oʻrganish uchun davom eting.
