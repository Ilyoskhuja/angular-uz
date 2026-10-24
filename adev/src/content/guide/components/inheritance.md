# Meros (Inheritance)

TIP: Bu qoʻllanma siz [Asosiy tushunchalar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Angular komponentlari TypeScript klasslari boʻlib, JavaScript'ning standart meros (inheritance) semantikasida ishtirok etadi.

Komponent istalgan asosiy klassni kengaytirishi mumkin:

```ts
export class ListboxBase {
  value: string;
}

@Component(/* ... */)
export class CustomListbox extends ListboxBase {
  // CustomListbox inherits the `value` property.
}
```

## Boshqa komponentlar va direktivalarni kengaytirish {#extending-other-components-and-directives}

Komponent boshqa komponent yoki direktivani kengaytirganda, u asosiy klass dekoratorida eʼlon qilingan metadataning bir qismini va asosiy klassning dekorator bilan belgilangan aʼzolarini meros qilib oladi. Bunga host bogʻlashlari, input'lar, output'lar va hayot sikli metodlari kiradi.

```angular-ts
@Component({
  selector: 'base-listbox',
  template: ` ... `,
  host: {
    '(keydown)': 'handleKey($event)',
  },
})
export class ListboxBase {
  value = input.required<string>();
  handleKey(event: KeyboardEvent) {
    /* ... */
  }
}

@Component({
  selector: 'custom-listbox',
  template: ` ... `,
  host: {
    '(click)': 'focusActiveOption()',
  },
})
export class CustomListbox extends ListboxBase {
  disabled = input(false);
  focusActiveOption() {
    /* ... */
  }
}
```

Yuqoridagi misolda `CustomListbox` `ListboxBase` bilan bogʻliq barcha maʼlumotlarni meros qilib oladi va selektor hamda shablonni oʻz qiymatlari bilan qayta belgilaydi. `CustomListbox` ikkita input'ga (`value` va `disabled`) va ikkita hodisa tinglovchisiga (`keydown` va `click`) ega.

Bola klasslar natijada oʻz ajdodlarining barcha input'lari, output'lari va host bogʻlashlari hamda oʻzlarinikining _birlashmasiga_ ega boʻladi.

### Inyeksiya qilingan bogʻliqliklarni uzatish {#forwarding-injected-dependencies}

Asosiy klass `inject()`'ni xususiyat initsializatori sifatida ishlatganda, bola klass bu xususiyatni avtomatik meros qilib oladi. `super` orqali uzatish talab qilinmaydi.

```ts
@Component(/* ... */)
export class ListboxBase {
  protected element = inject(ElementRef);
}

@Component(/* ... */)
export class CustomListbox extends ListboxBase {
  // `element` is inherited from `ListboxBase`.
}
```

Agar asosiy klass bogʻliqliklarni konstruktor parametrlari sifatida inyeksiya qilsa, bola klass bu bogʻliqliklarni `super`'ga aniq uzatishi shart.

```ts
@Component(/* ... */)
export class ListboxBase {
  constructor(private element: ElementRef) {}
}

@Component(/* ... */)
export class CustomListbox extends ListboxBase {
  constructor(element: ElementRef) {
    super(element);
  }
}
```

### Hayot sikli metodlarini qayta belgilash {#overriding-lifecycle-methods}

Agar asosiy klass `ngOnInit` kabi hayot sikli metodini eʼlon qilsa, `ngOnInit`'ni ham amalga oshiradigan bola klass asosiy klassning implementatsiyasini _qayta belgilaydi_ (overrides). Agar asosiy klassning hayot sikli metodini saqlab qolmoqchi boʻlsangiz, metodni `super` orqali aniq chaqiring:

```ts
@Component(/* ... */)
export class ListboxBase {
  protected isInitialized = false;
  ngOnInit() {
    this.isInitialized = true;
  }
}

@Component(/* ... */)
export class CustomListbox extends ListboxBase {
  override ngOnInit() {
    super.ngOnInit();
    /* ... */
  }
}
```
