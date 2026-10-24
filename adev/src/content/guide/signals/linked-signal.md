# `linkedSignal` bilan bogʻliq holat

Angular kodingizda biror holatni saqlash uchun `signal` funksiyasidan foydalanishingiz mumkin. Baʼzan bu holat biror _boshqa_ holatga bogʻliq boʻladi. Masalan, foydalanuvchiga buyurtma uchun yetkazib berish usulini tanlash imkonini beruvchi komponentni tasavvur qiling:

```typescript
@Component({
  /* ... */
})
export class ShippingMethodPicker {
  shippingOptions: Signal<ShippingMethod[]> = getShippingOptions();

  // Select the first shipping option by default.
  selectedOption = signal(this.shippingOptions()[0]);

  changeShipping(newOptionIndex: number) {
    this.selectedOption.set(this.shippingOptions()[newOptionIndex]);
  }
}
```

Bu misolda `selectedOption` sukut boʻyicha birinchi variantga teng, lekin foydalanuvchi boshqa variantni tanlasa oʻzgaradi. Biroq `shippingOptions` — signal, uning qiymati oʻzgarishi mumkin! Agar `shippingOptions` oʻzgarsa, `selectedOption` endi yaroqli variant boʻlmagan qiymatni saqlab qolishi mumkin.

**`linkedSignal` funksiyasi biror boshqa holat bilan tubdan _bogʻlangan_ holatni saqlash uchun signal yaratish imkonini beradi.** Yuqoridagi misolga qaytsak, `linkedSignal` `signal`'ning oʻrnini bosa oladi:

```ts
@Component({
  /* ... */
})
export class ShippingMethodPicker {
  shippingOptions: Signal<ShippingMethod[]> = getShippingOptions();

  // Initialize selectedOption to the first shipping option.
  selectedOption = linkedSignal(() => this.shippingOptions()[0]);

  changeShipping(index: number) {
    this.selectedOption.set(this.shippingOptions()[index]);
  }
}
```

`linkedSignal` `signal`'ga oʻxshab ishlaydi, lekin bitta asosiy farq bilan — sukut qiymatini uzatish oʻrniga, `computed`'dagi kabi, _hisoblash funksiyasini_ (computation function) uzatasiz. Hisoblash qiymati oʻzgarganda `linkedSignal`'ning qiymati hisoblash natijasiga oʻzgaradi. Bu `linkedSignal` har doim yaroqli qiymatga ega boʻlishini taʼminlashga yordam beradi.

Quyidagi misol `linkedSignal`'ning qiymati u bogʻlangan holatga qarab qanday oʻzgarishi mumkinligini koʻrsatadi:

```ts
const shippingOptions = signal(['Ground', 'Air', 'Sea']);
const selectedOption = linkedSignal(() => shippingOptions()[0]);
console.log(selectedOption()); // 'Ground'

selectedOption.set(shippingOptions()[2]);
console.log(selectedOption()); // 'Sea'

shippingOptions.set(['Email', 'Will Call', 'Postal service']);
console.log(selectedOption()); // 'Email'
```

## Oldingi holatni hisobga olish {#accounting-for-previous-state}

Baʼzi hollarda `linkedSignal` uchun hisoblash `linkedSignal`'ning oldingi qiymatini hisobga olishi kerak boʻladi.

Yuqoridagi misolda `shippingOptions` oʻzgarganda `selectedOption` har doim birinchi variantga qaytib yangilanadi. Biroq, agar foydalanuvchi tanlagan variant hali ham roʻyxatning qayeridadir mavjud boʻlsa, uning tanlovini saqlab qolishni istashingiz mumkin. Bunga erishish uchun alohida _source_ (manba) va _computation_ (hisoblash) bilan `linkedSignal` yaratishingiz mumkin:

```ts
interface ShippingMethod {
  id: number;
  name: string;
}

@Component({
  /* ... */
})
export class ShippingMethodPicker {
  constructor() {
    this.changeShipping(2);
    this.changeShippingOptions();
    console.log(this.selectedOption()); // {"id":2,"name":"Postal Service"}
  }

  shippingOptions = signal<ShippingMethod[]>([
    {id: 0, name: 'Ground'},
    {id: 1, name: 'Air'},
    {id: 2, name: 'Sea'},
  ]);

  selectedOption = linkedSignal<ShippingMethod[], ShippingMethod>({
    // `selectedOption` is set to the `computation` result whenever this `source` changes.
    source: this.shippingOptions,
    computation: (newOptions, previous) => {
      // If the newOptions contain the previously selected option, preserve that selection.
      // Otherwise, default to the first option.
      return newOptions.find((opt) => opt.id === previous?.value.id) ?? newOptions[0];
    },
  });

  changeShipping(index: number) {
    this.selectedOption.set(this.shippingOptions()[index]);
  }

  changeShippingOptions() {
    this.shippingOptions.set([
      {id: 0, name: 'Email'},
      {id: 1, name: 'Sea'},
      {id: 2, name: 'Postal Service'},
    ]);
  }
}
```

`linkedSignal` yaratganingizda, faqat hisoblashni berish oʻrniga alohida `source` va `computation` xususiyatlariga ega obyekt uzatishingiz mumkin.

`source` har qanday signal boʻlishi mumkin, masalan `computed` yoki komponent `input`'i. `linkedSignal` `source` oʻzgarganda yoki `computation`'da murojaat qilingan har qanday signal oʻzgarganda oʻz qiymatini berilgan `computation` natijasi bilan yangilaydi.

`computation` — `source`'ning yangi qiymatini va `previous` obyektini qabul qiluvchi funksiya. `previous` obyekti ikki xususiyatga ega — `previous.source` `source`'ning oldingi qiymati, `previous.value` esa `linkedSignal`'ning oldingi qiymati. Bu oldingi qiymatlardan hisoblashning yangi natijasini aniqlash uchun foydalanishingiz mumkin.

HELPFUL: `previous` parametridan foydalanganda `linkedSignal`'ning generik tur argumentlarini aniq koʻrsatish zarur. Birinchi generik tur `source` turiga mos keladi, ikkinchi generik tur esa `computation`'ning chiqish turini belgilaydi.

## Maxsus tenglik taqqoslashi {#custom-equality-comparison}

`linkedSignal`, har qanday boshqa signal kabi, maxsus tenglik funksiyasi bilan sozlanishi mumkin. Bu funksiya quyi oqimdagi bogʻliqliklar tomonidan `linkedSignal` qiymati (hisoblash natijasi) oʻzgarganini aniqlash uchun ishlatiladi:

```typescript
const activeUser = signal({id: 123, name: 'Morgan', isAdmin: true});

const activeUserEditCopy = linkedSignal(() => activeUser(), {
  // Consider the user as the same if it's the same `id`.
  equal: (a, b) => a.id === b.id,
});

// Or, if separating `source` and `computation`
const activeUserEditCopy = linkedSignal({
  source: activeUser,
  computation: (user) => user,
  equal: (a, b) => a.id === b.id,
});
```

## set operatsiyasini moslashtirish {#customizing-the-set-operation}

Baʼzan `linkedSignal`'ning `set` va `update` operatsiyalari `linkedSignal`'ning qiymatini bevosita yangilash oʻrniga haqiqat manbasiga (source of truth) qayta yozishini istashingiz mumkin. Bu xatti-harakatni opsiyalarda `set` funksiyasini uzatish orqali moslashtirishingiz mumkin.

Maxsus `set` funksiyasi ikki argument qabul qiladi:

1. Oʻrnatilayotgan yangi qiymat.
2. `rawSet` funksiyasi — uni `linkedSignal`'ning ichki holatini bevosita yangilash uchun chaqirishingiz mumkin (sukut boʻyicha xatti-harakatga mos).

NOTE: `rawSet`'dan foydalanish `linkedSignal`'ning qiymatini bevosita yangilash imkonini beradi. Bu hisoblashning ishga tushishini oldini olish uchun foydali boʻlishi mumkin, masalan, agar u qimmat hosil qilish boʻlsa va natijani allaqachon bilsangiz.

### Manba signaliga qayta yozish {#writing-back-to-a-source-signal}

Temperaturani Farengeytda koʻrsatuvchi va tahrirlash imkonini beruvchi, lekin haqiqat manbasi sifatida Selsiy signalidan foydalanuvchi komponentni koʻrib chiqaylik:

```typescript
const tempC = signal(0);
const tempF = linkedSignal(() => (tempC() * 9) / 5 + 32, {
  set: (valF) => tempC.set(((valF - 32) * 5) / 9),
});

console.log(tempF()); // 32

// Setting Fahrenheit updates Celsius, which reactively updates Fahrenheit
tempF.set(212);
console.log(tempC()); // 100
console.log(tempF()); // 212
```

### Ota obyekt ichidagi xususiyatni yangilash {#updating-a-property-inside-a-parent-object}

Yana bir keng tarqalgan holat — ota obyekt ichidagi muayyan xususiyatni yangilash. Ota obyekt signalda saqlanadi va siz ichki (nested) xususiyatga bogʻlanasiz:

```typescript
interface Order {
  id: number;
  shippingMethod: string;
}

const order = signal<Order>({
  id: 42,
  shippingMethod: 'Ground',
});

const shippingMethod = linkedSignal(() => order().shippingMethod, {
  set: (newMethod) => {
    // Perform an immutable update to write the change back to the order
    order.update((currentOrder) => ({
      ...currentOrder,
      shippingMethod: newMethod,
    }));
  },
});

console.log(shippingMethod()); // 'Ground'

// Updating the shippingMethod updates the parent order object
shippingMethod.set('Air');
console.log(order()); // { id: 42, shippingMethod: 'Air' }
console.log(shippingMethod()); // 'Air'
```
