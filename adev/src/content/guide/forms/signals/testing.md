# Signal Forms'ni testlash

Formalar koʻpincha ilovalar uchun juda muhim, testlash esa kod bazasi oʻzgarganda ham ularning toʻgʻri ishlashiga ishonch beradi. Signal Forms logikasining katta qismini shablonda emas, sxemada saqlaydi, bu esa forma xatti-harakatining aksariyatini komponentni render qilmasdan testlash imkonini beradi.

Bu qoʻllanma shunday testlarni qanday sozlashni koʻrsatadi: avval alohida logika testlari, keyin DOM bilan oʻzaro aloqa muhim boʻlgan holatlar uchun komponentga bogʻlangan testlar yoritiladi.

## Forma logikasini alohida testlash {#testing-form-logic-in-isolation}

Faqat validatsiya, oʻchirilgan (disabled) holat, majburiy (required) holat yoki xato chiqishini tekshirish kerak boʻlganda, komponentni render qilish oʻrniga formani bevosita testlang. Alohida testlar sozlashni kichik saqlaydi va testni formaning xatti-harakatiga qaratish imkonini beradi.

Asosiy talab — injector. Signal Forms forma yaratish vaqtida inyeksiya kontekstini talab qiladi. Agar test `form()`'ni usiz chaqirsa, chaqiruv test forma haqida biror narsani tekshirishga ulgurmasdan xato beradi.

Bu talabni qondirishning eng bevosita yoʻli — injector'ni aniq uzatish. Quyidagi test `required` qoidasi bilan forma yaratadi va maydon qiymat olgandan keyin valid boʻlishini tekshiradi:

```ts {header: 'profile-form.spec.ts'}
import {Injector, signal} from '@angular/core';
import {TestBed} from '@angular/core/testing';
import {form, required} from '@angular/forms/signals';
import {describe, expect, it} from 'vitest';

describe('profile form', () => {
  it('marks required fields as invalid until they have a value', () => {
    const model = signal({name: ''});

    const profileForm = form(
      model,
      (path) => {
        required(path.name);
      },
      {injector: TestBed.inject(Injector)},
    );

    expect(profileForm.name().valid()).toBe(false);
    expect(profileForm.name().errors()).toEqual([expect.objectContaining({kind: 'required'})]);

    profileForm.name().value.set('Ada');

    expect(profileForm.name().valid()).toBe(true);
    expect(profileForm.name().errors()).toEqual([]);
  });
});
```

Bu namuna aksariyat alohida testlar uchun yaxshi ishlaydi, chunki injector talabi chaqiruv joyida koʻrinib turadi. Shuningdek, u Angular manba kodidagi Signal Forms unit testlarining formalarni qanday yaratishini ham aks ettiradi.

Testlanayotgan kod `form()`'ni ichkarida chaqirsa, injector'ni bevosita uzata olmasligingiz mumkin. Bunday holda chaqiruvni atrofdagi (ambient) inyeksiya kontekstiga oʻrang:

```ts {header: 'profile-form.spec.ts'}
import {signal} from '@angular/core';
import {TestBed} from '@angular/core/testing';
import {form, required} from '@angular/forms/signals';
import {describe, expect, it} from 'vitest';

describe('profile form', () => {
  it('can create a form inside an injection context', () => {
    const model = signal({name: ''});

    TestBed.runInInjectionContext(() => {
      const profileForm = form(model, (path) => {
        required(path.name);
      });

      expect(profileForm.name().valid()).toBe(false);
    });
  });
});
```

Ikkala namuna ham bir xil turdagi forma hosil qiladi. Test formani bevosita yaratganda `{injector}` uzatish koʻpincha eng tushunarli tanlov hisoblanadi. `TestBed.runInInjectionContext()` esa testlanayotgan kod `form()`'ni ichkarida chaqirganda va siz atrofdagi inyeksiya kontekstini taʼminlashingiz kerak boʻlganda foydali.

Forma yaratilgach, uni maydon holati signallari orqali testlang. Keng tarqalgan tekshiruvlar `valid()`, `invalid()`, `disabled()`, `required()` va `errors()`'ni oʻz ichiga oladi. Aksariyat forma logikasi uchun bu xatti-harakatni DOM'ni jalb qilmasdan tekshirishga yetarli.

## Bir nechta qoidali formani testlash {#testing-a-form-with-multiple-rules}

Injector sozlangandan keyin yaxshi keyingi qadam — forma logikasining bir necha qismini birga sinaydigan toʻliq test. Bunday test hamon alohida, lekin u haqiqiy ilova formasiga ancha yaqinroq koʻrinadi.

Masalan, bu test asosiy majburiylik qoidasini ham, boshqa maydonga bogʻliq boʻlgan shartli majburiylik qoidasini ham tekshiradi:

```ts {header: 'profile-form.spec.ts'}
import {Injector, signal} from '@angular/core';
import {TestBed} from '@angular/core/testing';
import {form, required} from '@angular/forms/signals';
import {describe, expect, it} from 'vitest';

describe('profile form', () => {
  it('updates validation state when related fields change', () => {
    const model = signal({
      name: '',
      age: 5,
    });

    const profileForm = form(
      model,
      (path) => {
        required(path.name);
        required(path.name, {
          error: (ctx) => ({kind: `required-${ctx.valueOf(path.age)}`}),
          when: ({valueOf}) => valueOf(path.age) > 10,
        });
      },
      {injector: TestBed.inject(Injector)},
    );

    expect(profileForm.name().invalid()).toBe(true);
    expect(profileForm.name().errors()).toEqual([expect.objectContaining({kind: 'required'})]);

    profileForm.age().value.set(15);

    expect(profileForm.name().errors()).toEqual([
      expect.objectContaining({kind: 'required'}),
      expect.objectContaining({kind: 'required-15'}),
    ]);

    profileForm.name().value.set('Ada');

    expect(profileForm.name().valid()).toBe(true);
    expect(profileForm.name().errors()).toEqual([]);
  });
});
```

Bu misol muhim testlash namunasini koʻrsatadi: bir maydonni yangilang, keyin boshqa maydonning holatini tekshiring. Signal Forms qoidalari reaktiv boʻlgani uchun maydon validatsiyasi qoʻshni qiymatlarga, yuqori darajadagi (parent) qiymatlarga yoki boshqa hosilaviy shartlarga bogʻliq boʻlishi mumkin. Testlar faqat oʻzgargan maydonni tekshirish oʻrniga bu bogʻliqliklarni bevosita tekshirishi kerak.

Validatsiyaga qaratilgan testlar uchun `errors()` odatda eng foydali tekshiruv hisoblanadi. `valid()` va `invalid()` maydon hozir validatsiyadan oʻtyaptimi-yoʻqmi ekanligini aytadi, `errors()` esa qaysi qoida muvaffaqiyatsizlikka sabab boʻlganini koʻrsatadi. Maydonda bir nechta validator yoki shartli qoidalar boʻlganda bu ayniqsa foydali boʻladi.

Xuddi shu tuzilma aksariyat kundalik forma testlari uchun ishlaydi:

1. Xatti-harakatni takrorlaydigan eng kichik tuzilmali model signalini yarating.
1. Formani aniq injector bilan quring.
1. Maydonning dastlabki holatini tekshiring.
1. Maydonni `.value.set(...)` bilan oʻzgartiring; maydonlararo qoidalarni testlashda qoʻshni maydonlarni ham oʻzgartiring.
1. Yangilangan holat signallarini, odatda `errors()`, `valid()` yoki `invalid()`'ni tekshiring.

Test render qilish haqida emas, sxema xatti-harakati haqida boʻlsa, sukut boʻyicha shu alohida uslubni tanlang. Bu komponent testidan tezroq va xatti-harakat oʻzgarganda qaysi qoida bunga javobgar ekanligini koʻrishni osonlashtiradi.

## Komponentlarga bogʻlangan formalarni testlash {#testing-forms-bound-to-components}

Shablon bogʻlashlariga, `dispatchEvent` orqali foydalanuvchi oʻzaro aloqasiga yoki oʻz renderini oʻzi boshqaradigan maxsus forma kontrollariga bogʻliq xatti-harakatni tekshirish kerak boʻlganda alohida testlar yetarli emas. Haqiqiy DOM elementlari bilan oʻzaro aloqa qilish uchun shablonni render qiladigan komponentga bogʻlangan testlar kerak boʻladi.

### Komponent testini sozlash {#setting-up-a-component-test}

Komponentga bogʻlangan testlar komponentni render qiladi, shunda siz haqiqiy DOM elementlari bilan oʻzaro aloqa qila olasiz. Komponentni `TestBed.createComponent()` bilan yarating va tekshirishdan oldin render yakunlanishini kuting:

```angular-ts {header: 'profile-form.ts'}
import {Component, signal} from '@angular/core';
import {form, FormField, required} from '@angular/forms/signals';

@Component({
  selector: 'app-profile-form',
  imports: [FormField],
  template: `<input [formField]="profileForm.name" />`,
})
export class ProfileForm {
  readonly model = signal({name: 'Ada'});
  readonly profileForm = form(this.model, (path) => {
    required(path.name);
  });
}
```

```ts {header: 'profile-form.spec.ts'}
import {TestBed} from '@angular/core/testing';
import {describe, expect, it} from 'vitest';
import {ProfileForm} from './profile-form';

describe('ProfileForm', () => {
  it('reflects model values in the DOM and updates the model on user input', async () => {
    const fixture = TestBed.createComponent(ProfileForm);
    await fixture.whenStable();

    const input = fixture.nativeElement.querySelector('input') as HTMLInputElement;

    // Model → View: the input reflects the model's initial value
    expect(input.value).toBe('Ada');

    // View → Model: simulate the user clearing the field
    input.value = '';
    input.dispatchEvent(new Event('input'));
    await fixture.whenStable();

    expect(fixture.componentInstance.profileForm.name().value()).toBe('');
    expect(fixture.componentInstance.profileForm.name().valid()).toBe(false);
  });
});
```

Eʼtibor bering, komponent `form()`'ni aniq injector'siz ishlatadi, chunki komponentning oʻz inyeksiya konteksti uni avtomatik taʼminlaydi. Har bir oʻzgarishdan keyin `await fixture.whenStable()` tekshirishdan oldin render va effect'lar yakunlanishini kutadi.

Xuddi shu namuna asinxron validatorlar yoki server chaqiruvlari kabi asinxron operatsiyalar uchun ham ishlaydi. Asinxron ish yakunlangandan keyin `await fixture.whenStable()`'ni chaqiring.

## Har bir yondashuvdan qachon foydalanish kerak {#when-to-use-each-approach}

| Nimani tekshirish kerak                                | Yondashuv              |
| ---------------------------------------------------- | --------------- |
| Validatsiya qoidalari, `errors()`, `valid()`, `invalid()` | Alohida        |
| Oʻchirilgan, majburiy yoki faqat oʻqish uchun holat   | Alohida        |
| Maydonlararo reaktiv bogʻliqliklar                    | Alohida        |
| Shartli sxemalar (`applyWhen`, `applyWhenValue`)      | Alohida        |
| Input qiymatlarining DOM'da render qilinishi          | Komponentga bogʻlangan |
| Foydalanuvchi yozishining modelni yangilashi          | Komponentga bogʻlangan |
| Oʻz shablonlariga ega maxsus forma kontrollari        | Komponentga bogʻlangan |
| Fokusni boshqarish yoki accessibility atributlari     | Komponentga bogʻlangan |

Aksariyat formalarga faqat alohida testlar kifoya. Formaning logikasi (validatsiya, oʻchirilgan holat, maydonlararo qoidalar kabi) sxemada yashaydi, sxemalar esa ishlash uchun shablonga muhtoj emas. Komponentga bogʻlangan testlar sizni qiziqtirgan xatti-harakat forma va DOM oʻrtasidagi chegarani kesib oʻtganda qoʻshimcha qiymat beradi.

## Keyingi qadamlar {#next-steps}

Bu qoʻllanma Signal Forms'ni alohida va komponent shablonlari bilan testlashni qamrab oldi. Signal Forms'ning boshqa jihatlarini yorituvchi tegishli qoʻllanmalar:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/form-submission" title="Forma yuborish" />
</docs-pill-row>
