# Komponent output xususiyatlari

Komponentlar bilan ishlashda boshqa komponentlarga nimadir sodir boʻlgani haqida xabar berish kerak boʻlishi mumkin. Masalan, tugma bosilgan, roʻyxatga element qoʻshilgan/olib tashlangan yoki boshqa muhim yangilanish yuz bergan boʻlishi mumkin. Bunday vaziyatda komponentlar ota komponentlar bilan muloqot qilishi kerak.

Angular bunday xatti-harakatni taʼminlash uchun `output()` funksiyasidan foydalanadi.

NOTE: [Outputlar qoʻllanmasida maxsus hodisalar](/guide/components/outputs) haqida koʻproq bilib oling.

Bu mashgʻulotda komponentlar bilan muloqot qilish uchun `output()` funksiyasidan qanday foydalanishni oʻrganasiz.

<hr />

Bola komponentdan ota komponentga muloqot yoʻlini yaratish uchun klass xususiyatini ishga tushirishda `output` funksiyasidan foydalaning.

```ts {header:"child.ts"}
@Component({...})
class Child {
  incrementCountEvent = output<number>();
}
```

Endi komponent ota komponent tinglashi mumkin boʻlgan hodisalarni hosil qila oladi. Hodisalarni `emit` metodini chaqirish orqali ishga tushiring:

```ts {header:"child.ts"}
class Child {
  ...

  onClick() {
    this.count++;
    this.incrementCountEvent.emit(this.count);
  }
}
```

emit funksiyasi `output`'da aniqlangan tur bilan bir xil turdagi hodisa hosil qiladi.

Xoʻsh, endi oʻzingiz sinab koʻring. Quyidagi vazifalarni bajarib, kodni toʻldiring:

<docs-workflow>

<docs-step title="`output()` xususiyatini qoʻshing {#add-an-output-property}">
`child.ts`'ni `addItemEvent` nomli output xususiyati qoʻshib yangilang, output turini `string` qilib belgilashni unutmang.
</docs-step>

<docs-step title="`addItem` metodini toʻldiring {#complete-additem-method}">
`child.ts`'da `addItem` metodini yangilang; logika sifatida quyidagi koddan foydalaning:

```ts {header:"child.ts", highlight:[2]}
addItem() {
  this.addItemEvent.emit('🐢');
}
```

</docs-step>

<docs-step title="`App` shablonini yangilang {#update-the-app-template}">
`app.ts`'da shablonni quyidagi kodni qoʻshib, chiqarilgan (emit qilingan) hodisani tinglaydigan qilib yangilang:

```angular-html
<app-child (addItemEvent)="addItem($event)" />
```

Endi "Add Item" tugmasi har safar bosilganda roʻyxatga yangi element qoʻshadi.

</docs-step>

</docs-workflow>

Zoʻr, shu bosqichda komponentlar asoslarini tugatdingiz — taʼsirli 👏

Angular'ning yana koʻplab ajoyib imkoniyatlarini ochish uchun oʻrganishda davom eting.
