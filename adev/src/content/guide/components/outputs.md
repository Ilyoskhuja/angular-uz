# Output'lar bilan maxsus hodisalar

TIP: Bu qoʻllanma siz [Asoslar qoʻllanmasini](essentials) allaqachon oʻqigansiz deb hisoblaydi. Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Angular komponentlari xususiyatga `output` funksiyasini tayinlash orqali maxsus hodisalarni (custom events) aniqlashi mumkin:

```ts {highlight:[5]}
@Component({
  /*...*/
})
export class ExpandablePanel {
  panelClosed = output<void>();
}
```

```angular-html
<expandable-panel (panelClosed)="savePanelState()" />
```

`output` funksiyasi `OutputEmitterRef` qaytaradi. `OutputEmitterRef`'ning `emit` metodini chaqirib, hodisani yuborishingiz (emit) mumkin:

```ts
this.panelClosed.emit();
```

Angular `output` funksiyasi bilan boshlangʻich qiymat berilgan xususiyatlarni **output'lar** deb ataydi. Output'lardan `click` kabi brauzerning oʻrnatilgan hodisalariga oʻxshash maxsus hodisalarni chaqirish uchun foydalanishingiz mumkin.

**Angular'ning maxsus hodisalari DOM boʻylab yuqoriga koʻtarilmaydi (bubble).**

**Output nomlari katta-kichik harfga sezgir.**

Komponent klassini kengaytirganda **output'lar bola klassga meros boʻlib oʻtadi.**

`output` funksiyasi Angular kompilyatori uchun alohida maʼnoga ega. **`output`'ni faqat komponent va direktiva xususiyatlarining boshlangʻich qiymatlarini berishda (property initializer) chaqirish mumkin.**

## Hodisa maʼlumotlarini yuborish {#emitting-event-data}

`emit`'ni chaqirganda hodisa maʼlumotlarini uzatishingiz mumkin:

```ts
// You can emit primitive values.
this.valueChanged.emit(7);

// You can emit custom event objects
this.thumbDropped.emit({
  pointerX: 123,
  pointerY: 456,
});
```

Shablonda hodisa tinglovchisini aniqlaganda hodisa maʼlumotlariga `$event` oʻzgaruvchisi orqali murojaat qilishingiz mumkin:

```angular-html
<custom-slider (valueChanged)="logValue($event)" />
```

Hodisa maʼlumotlarini ota komponentda qabul qiling:

```ts
@Component({
 /*...*/
})
export class App {
  logValue(value: number) {
    ...
  }
}

```

## Output nomlarini sozlash {#customizing-output-names}

`output` funksiyasi shablonda hodisa uchun boshqa nom koʻrsatish imkonini beruvchi parametrni qabul qiladi:

```ts
@Component(/* ... */)
export class CustomSlider {
  changed = output({alias: 'valueChanged'});
}
```

```angular-html
<custom-slider (valueChanged)="saveVolume()" />
```

Bu taxallus (alias) xususiyatning TypeScript kodida ishlatilishiga taʼsir qilmaydi.

Odatda komponentlar uchun output'larga taxallus berishdan qochish kerak boʻlsa-da, bu imkoniyat asl nom uchun taxallusni saqlab qolgan holda xususiyatlarni qayta nomlashda yoki oʻrnatilgan DOM hodisalari nomi bilan toʻqnashuvlardan qochishda foydali boʻlishi mumkin.

## Output'larga dasturiy ravishda obuna boʻlish {#subscribing-to-outputs-programmatically}

Komponentni dinamik ravishda yaratganda komponent nusxasining output hodisalariga dasturiy ravishda obuna boʻlishingiz mumkin. `OutputRef` turi `subscribe` metodini oʻz ichiga oladi:

```ts
const someComponentRef: ComponentRef<SomeComponent> = viewContainerRef.createComponent(/*...*/);

someComponentRef.instance.someEventProperty.subscribe((eventData) => {
  console.log(eventData);
});
```

Angular obunachilari bor komponentlarni yoʻq qilganda hodisa obunalarini avtomatik tozalaydi. Shuningdek, hodisadan qoʻlda obunani bekor qilishingiz ham mumkin. `subscribe` funksiyasi `unsubscribe` metodiga ega `OutputRefSubscription` qaytaradi:

```ts
const eventSubscription = someComponent.someEventProperty.subscribe((eventData) => {
  console.log(eventData);
});

// ...

eventSubscription.unsubscribe();
```

## Hodisa nomlarini tanlash {#choosing-event-names}

HTMLElement kabi DOM elementlaridagi hodisalar bilan toʻqnashadigan output nomlarini tanlashdan qoching. Nomlar toʻqnashuvi bogʻlangan xususiyat komponentga tegishlimi yoki DOM elementigami degan chalkashlikni keltirib chiqaradi.

Komponent selektorlarida qilganingizdek, komponent output'lariga prefiks qoʻshishdan qoching. Bitta element faqat bitta komponentni host qila olgani uchun har qanday maxsus xususiyat komponentga tegishli deb hisoblanishi mumkin.

Output nomlari uchun doimo [camelCase](https://en.wikipedia.org/wiki/Camel_case) ishlating. Output nomlarini "on" prefiksi bilan boshlashdan qoching.

## Output'lardan RxJS bilan foydalanish {#using-outputs-with-rxjs}

Output'lar va RxJS oʻrtasidagi oʻzaro moslik haqida batafsil maʼlumot uchun [Komponent va direktiva output'larining RxJS bilan oʻzaro mosligi](ecosystem/rxjs-interop/output-interop) boʻlimiga qarang.

## Output'larni `@Output` dekoratori bilan eʼlon qilish {#declaring-outputs-with-the-output-decorator}

TIP: Angular jamoasi yangi loyihalar uchun `output` funksiyasidan foydalanishni tavsiya qilsa-da, dekoratorga asoslangan asl `@Output` API toʻliq qoʻllab-quvvatlanishda davom etadi.

Shuningdek, xususiyatga yangi `EventEmitter` tayinlab va `@Output` dekoratorini qoʻshib ham maxsus hodisalarni aniqlashingiz mumkin:

```ts
@Component(/* ... */)
export class ExpandablePanel {
  @Output() panelClosed = new EventEmitter<void>();
}
```

`EventEmitter`'ning `emit` metodini chaqirib, hodisani yuborishingiz mumkin.

### `@Output` dekoratori bilan taxalluslar {#aliases-with-the-output-decorator}

`@Output` dekoratori shablonda hodisa uchun boshqa nom koʻrsatish imkonini beruvchi parametrni qabul qiladi:

```ts
@Component(/* ... */)
export class CustomSlider {
  @Output('valueChanged') changed = new EventEmitter<number>();
}
```

```angular-html
<custom-slider (valueChanged)="saveVolume()" />
```

Bu taxallus xususiyatning TypeScript kodida ishlatilishiga taʼsir qilmaydi.

## Output'larni `@Component` dekoratorida koʻrsatish {#specify-outputs-in-the-component-decorator}

`@Output` dekoratoridan tashqari, komponent output'larini `@Component` dekoratoridagi `outputs` xususiyati orqali ham koʻrsatishingiz mumkin. Bu komponent xususiyatni asos klassdan meros qilib olganda foydali boʻlishi mumkin:

```ts
// `CustomSlider` inherits the `valueChanged` property from `BaseSlider`.
@Component({
  /*...*/
  outputs: ['valueChanged'],
})
export class CustomSlider extends BaseSlider {}
```

Bundan tashqari, `outputs` roʻyxatida satr ichida ikki nuqtadan keyin taxallusni yozib, output taxallusini ham koʻrsatishingiz mumkin:

```ts
// `CustomSlider` inherits the `valueChanged` property from `BaseSlider`.
@Component({
  /*...*/
  outputs: ['valueChanged: volumeChanged'],
})
export class CustomSlider extends BaseSlider {}
```
