# Formalarni validatsiya qilish

Formalar bilan ishlashda yana bir keng tarqalgan holat — toʻgʻri maʼlumotlar yuborilishini taʼminlash uchun kiritmalarni validatsiya qilish zarurati.

NOTE: [Chuqur qoʻllanmada forma kiritmalarini validatsiya qilish](/guide/forms/reactive-forms#validating-form-input) haqida koʻproq bilib oling.

Bu mashgʻulotda reaktiv formalar yordamida formalarni qanday validatsiya qilishni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="Validators'ni import qiling {#import-validators}">

Angular validatsiya vositalari toʻplamini taqdim etadi. Ulardan foydalanish uchun avval komponentni `@angular/forms`'dan `Validators`'ni import qilish uchun yangilang.

```ts {highlight:[1]}
import {ReactiveFormsModule, Validators} from '@angular/forms';

@Component({...})
export class App {}
```

</docs-step>

<docs-step title="Formaga validatsiya qoʻshing {#add-validation-to-form}">

Har bir `FormControl`'ga uning qiymatlarini validatsiya qilish uchun ishlatmoqchi boʻlgan `Validators`'ni uzatish mumkin. Masalan, `profileForm`'dagi `name` maydonini majburiy qilmoqchi boʻlsangiz, `Validators.required`'dan foydalaning.
Angular formamizdagi `email` maydoni uchun biz uning boʻsh qoldirilmasligini va toʻgʻri elektron pochta manzili tuzilmasiga mos kelishini taʼminlamoqchimiz. Bunga `Validators.required` va `Validators.email` validatorlarini massivda birlashtirish orqali erishishimiz mumkin.
`name` va `email` `FormControl`'larini yangilang:

```ts
profileForm = new FormGroup({
  name: new FormControl('', Validators.required),
  email: new FormControl('', [Validators.required, Validators.email]),
});
```

</docs-step>

<docs-step title="Shablonda forma validatsiyasini tekshiring {#check-form-validation-in-template}">

Forma yaroqli (valid) ekanligini aniqlash uchun `FormGroup` klassida `valid` xususiyati mavjud.
Bu xususiyatdan atributlarni dinamik bogʻlash uchun foydalanishingiz mumkin. Yuborish `button`'ini forma yaroqliligiga qarab yoqiladigan qilib yangilang.

```angular-html
<button type="submit" [disabled]="!profileForm.valid">Submit</button>
```

</docs-step>

</docs-workflow>

Endi reaktiv formalarda validatsiya qanday ishlashi haqidagi asoslarni bilasiz.

Angular'da formalar bilan ishlashning bu asosiy tushunchalarini oʻrganganingiz uchun ajoyib ish. Koʻproq bilmoqchi boʻlsangiz, [Angular formalar hujjatlariga](guide/forms/form-validation) qarang.
