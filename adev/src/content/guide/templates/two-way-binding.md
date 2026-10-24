# Ikki tomonlama bogʻlash

**Ikki tomonlama bogʻlash (two-way binding)** — bu qiymatni elementga bogʻlash bilan bir vaqtda oʻsha elementga oʻzgarishlarni shu bogʻlash orqali orqaga uzatish imkonini ham beruvchi qisqa yozuv.

## Sintaksis {#syntax}

Ikki tomonlama bogʻlash sintaksisi kvadrat qavslar va oddiy qavslarning birikmasidir: `[()]`. U xususiyat bogʻlash sintaksisi `[]` va hodisa bogʻlash sintaksisi `()`'ni birlashtiradi. Angular hamjamiyati bu sintaksisni norasmiy tarzda "banana-in-a-box" (qutidagi banan) deb ataydi.

## Forma elementlari bilan ikki tomonlama bogʻlash {#two-way-binding-with-form-controls}

Dasturchilar odatda foydalanuvchi forma elementi (form control) bilan ishlayotganda komponent maʼlumotlarini u bilan sinxron saqlash uchun ikki tomonlama bogʻlashdan foydalanadilar. Masalan, foydalanuvchi matn maydonini toʻldirganda, bu komponentdagi holatni yangilashi kerak.

Quyidagi misol sahifadagi `firstName` atributini dinamik ravishda yangilaydi:

```angular-ts
import {Component} from '@angular/core';
import {FormsModule} from '@angular/forms';

@Component({
  imports: [FormsModule],
  template: `
    <main>
      <h2>Hello {{ firstName }}!</h2>
      <input type="text" [(ngModel)]="firstName" />
    </main>
  `,
})
export class App {
  firstName = 'Ada';
}
```

Native forma elementlari bilan ikki tomonlama bogʻlashdan foydalanish uchun quyidagilarni bajarishingiz kerak:

1. `@angular/forms`'dan `FormsModule`'ni import qiling
1. `ngModel` direktivasini ikki tomonlama bogʻlash sintaksisi bilan ishlating (masalan, `[(ngModel)]`)
1. Unga yangilanishini istagan holatni tayinlang (masalan, `firstName`)

Bu sozlangandan soʻng Angular matn maydonidagi har qanday yangilanish komponent holatida toʻgʻri aks etishini taʼminlaydi!

[`NgModel`](/api/forms/NgModel) haqida rasmiy hujjatlardan koʻproq bilib oling.

## Komponentlar oʻrtasida ikki tomonlama bogʻlash {#two-way-binding-between-components}

Ota va bola komponent oʻrtasida ikki tomonlama bogʻlashdan foydalanish forma elementlariga nisbatan koʻproq sozlashni talab qiladi.

Quyida `App` boshlangʻich hisoblagich holatini oʻrnatish uchun masʼul boʻlgan, lekin hisoblagichni yangilash va UI'ni render qilish mantigʻi asosan uning bola komponenti `Counter` ichida joylashgan misol keltirilgan.

```angular-ts {header: 'app.ts'}
import {Component} from '@angular/core';
import {Counter} from './counter';

@Component({
  selector: 'app-root',
  imports: [Counter],
  template: `
    <main>
      <h1>Counter: {{ initialCount }}</h1>
      <app-counter [(count)]="initialCount"></app-counter>
    </main>
  `,
})
export class App {
  initialCount = 18;
}
```

```angular-ts {header: 'counter.ts'}
import {Component, model} from '@angular/core';

@Component({
  selector: 'app-counter',
  template: `
    <button (click)="updateCount(-1)">-</button>
    <span>{{ count() }}</span>
    <button (click)="updateCount(+1)">+</button>
  `,
})
export class Counter {
  count = model<number>(0);

  updateCount(amount: number): void {
    this.count.update((currentCount) => currentCount + amount);
  }
}
```

### Komponentlar oʻrtasida ikki tomonlama bogʻlashni yoqish {#enabling-two-way-binding-between-components}

Yuqoridagi misolni asosiy qismlarga ajratsak, komponentlar uchun har bir ikki tomonlama bogʻlash quyidagilarni talab qiladi:

Bola komponentda `model` xususiyati boʻlishi shart.

Quyida soddalashtirilgan misol keltirilgan:

```angular-ts {header: 'counter.ts'}
import {Component, model} from '@angular/core';

@Component({
  /* Omitted for brevity */
})
export class Counter {
  count = model<number>(0);

  updateCount(amount: number): void {
    this.count.update((currentCount) => currentCount + amount);
  }
}
```

Ota komponent quyidagilarni bajarishi shart:

1. `model` xususiyati nomini ikki tomonlama bogʻlash sintaksisiga oʻrash.
1. `model` xususiyatiga xususiyat yoki signal tayinlash.

Quyida soddalashtirilgan misol keltirilgan:

```angular-ts {header: 'app.ts'}
import {Component} from '@angular/core';
import {Counter} from './counter';

@Component({
  selector: 'app-root',
  imports: [Counter],
  template: `
    <main>
      <app-counter [(count)]="initialCount"></app-counter>
    </main>
  `,
})
export class App {
  initialCount = 18;
}
```
