# Komponent input xususiyatlari

Baʼzan ilova yaratishda komponentga maʼlumot yuborish kerak boʻladi. Bu maʼlumotdan komponentni sozlash yoki, masalan, ota komponentdan bola komponentga axborot yuborish uchun foydalanish mumkin.

Angular `input` deb nomlangan tushunchadan foydalanadi. Bu boshqa freymvorklardagi `props`'ga oʻxshaydi. `input` xususiyatini yaratish uchun `input()` funksiyasidan foydalaning.

NOTE: [Inputlar qoʻllanmasida input xususiyatlari orqali maʼlumot qabul qilish](/guide/components/inputs) haqida koʻproq bilib oling.

Bu mashgʻulotda komponentlarga axborot yuborish uchun `input()` funksiyasidan qanday foydalanishni oʻrganasiz.

<hr>

`input` xususiyatini yaratish uchun komponent klassining xususiyatini ishga tushirishda `input()` funksiyasini qoʻshing:

```ts {header:"user.ts"}
class User {
  occupation = input<string>();
}
```

`input` orqali qiymat uzatishga tayyor boʻlganingizda, qiymatlarni shablonlarda atribut sintaksisi yordamida oʻrnatish mumkin. Misol:

```angular-ts {header:"app.ts", highlight:[3]}
@Component({
  ...
  template: `<app-user occupation="Angular Developer"></app-user>`
})
export class App {}
```

`input` funksiyasi `InputSignal` qaytaradi. Qiymatni signalni chaqirish orqali oʻqishingiz mumkin.

```angular-ts {header:"user.ts"}
@Component({
  ...
  template: `<p>The user's occupation is {{occupation()}}</p>`
})
```

<docs-workflow>

<docs-step title="`input()` xususiyatini aniqlang {#define-an-input-property}">
`user.ts`'dagi kodni `User`'da `name` nomli `input` xususiyatini aniqlaydigan va `string` turini koʻrsatadigan qilib yangilang. Hozircha boshlangʻich qiymat oʻrnatmang va `input()`'ni argumentlarsiz chaqiring. Shablonni gap oxirida `name` xususiyatini chaqirib interpolatsiya qiladigan qilib yangilashni unutmang.
</docs-step>

<docs-step title="`input` xususiyatiga qiymat uzating {#pass-a-value-to-the-input-property}">
`app.ts`'dagi kodni `name` xususiyatini `"Simran"` qiymati bilan yuboradigan qilib yangilang.
<br>

Kod muvaffaqiyatli yangilangach, ilova `The user's name is Simran` deb koʻrsatadi.
</docs-step>

</docs-workflow>

Bu ajoyib boʻlsa-da, komponentlar muloqotining faqat bir yoʻnalishi. Agar bola komponentdan ota komponentga axborot va maʼlumot yubormoqchi boʻlsangiz-chi? Bilish uchun keyingi darsga oʻting.

P.S. ajoyib ishlayapsiz — davom eting 🎉
