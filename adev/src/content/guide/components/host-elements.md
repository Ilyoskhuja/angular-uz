# Komponent host elementlari

TIP: Bu qoʻllanma siz [Asoslar qoʻllanmasini](essentials) allaqachon oʻqigansiz deb hisoblaydi. Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Angular komponent selektoriga mos keladigan har bir HTML elementi uchun komponent nusxasini yaratadi. Komponent selektoriga mos keladigan DOM elementi oʻsha komponentning **host elementi** hisoblanadi. Komponent shablonining mazmuni uning host elementi ichida render qilinadi.

```angular-ts
// Component source
@Component({
  selector: 'profile-photo',
  template: `<img src="profile-photo.jpg" alt="Your profile photo" />`,
})
export class ProfilePhoto {}
```

```angular-html
<!-- Using the component -->
<h3>Your profile photo</h3>
<profile-photo />
<button>Upload a new profile photo</button>
```

```angular-html
<!-- Rendered DOM -->
<h3>Your profile photo</h3>
<profile-photo>
  <img src="profile-photo.jpg" alt="Your profile photo" />
</profile-photo>
<button>Upload a new profile photo</button>
```

Yuqoridagi misolda `<profile-photo>` — `ProfilePhoto` komponentining host elementi.

## Host elementga bogʻlash {#binding-to-the-host-element}

Komponent oʻz host elementiga xususiyatlar, atributlar, stillar va hodisalarni bogʻlashi mumkin. Bu komponent shablonidagi elementlarga bogʻlash bilan bir xil ishlaydi, faqat `@Component` dekoratoridagi `host` xususiyati orqali aniqlanadi:

```angular-ts
@Component({
  ...,
  host: {
    'role': 'slider',
    '[attr.aria-valuenow]': 'value',
    '[class.active]': 'isActive()',
    '[style.background]' : `hasError() ? 'red' : 'green'`,
    '[tabIndex]': 'disabled ? -1 : 0',
    '(keydown)': 'updateValue($event)',
  },
})
export class CustomSlider {
  value: number = 0;
  disabled: boolean = false;
  isActive = signal(false);
  hasError = signal(false);
  updateValue(event: KeyboardEvent) { /* ... */ }

  /* ... */
}
```

NOTE: Hodisa nomi oldiga prefiks sifatida qoʻyish mumkin boʻlgan global maqsad (target) nomlari: `document:`, `window:` va `body:`.

NOTE: `'(keydown.enter)'` kabi tugma nomlari `KeyboardEvent.key` bilan solishtiriladi, bu esa foydalanuvchining klaviatura joylashuvi va kiritish tiliga bogʻliq. Joylashuvdan qatʼi nazar jismoniy tugmaga moslash uchun `code` modifikatoridan foydalaning, masalan `'(keydown.code.Enter)'`. Batafsil maʼlumot uchun [Tugma modifikatorlaridan foydalanish](guide/templates/event-listeners#using-key-modifiers) boʻlimiga qarang.

## `@HostBinding` va `@HostListener` dekoratorlari {#the-hostbinding-and-hostlistener-decorators}

Shuningdek, klass aʼzolariga `@HostBinding` va `@HostListener` dekoratorlarini qoʻllash orqali ham host elementga bogʻlashingiz mumkin.

`@HostBinding` host xususiyatlari va atributlarini xususiyatlar va getter'larga bogʻlash imkonini beradi:

```ts
@Component({/* ... */})
export class CustomSlider {
  @HostBinding('attr.aria-valuenow')
  value: number = 0;

  @HostBinding('tabIndex')
  get tabIndex() {
    return this.disabled ? -1 : 0;
  }

  /* ... */
}
```

`@HostListener` host elementga hodisa tinglovchilarini bogʻlash imkonini beradi. Dekorator hodisa nomini va ixtiyoriy argumentlar massivini qabul qiladi:

```ts
export class CustomSlider {
  @HostListener('keydown', ['$event'])
  updateValue(event: KeyboardEvent) {
    /* ... */
  }
}
```

<docs-callout critical title="Dekoratorlar oʻrniga `host` xususiyatidan foydalanishni afzal koʻring">
  **Doimo `@HostBinding` va `@HostListener` oʻrniga `host` xususiyatidan foydalanishni afzal koʻring.** Bu dekoratorlar faqat orqaga moslik (backwards compatibility) uchun mavjud.
</docs-callout>

## Bogʻlash toʻqnashuvlari {#binding-collisions}

Shablonda komponentdan foydalanganingizda oʻsha komponent nusxasining elementiga bogʻlashlar qoʻshishingiz mumkin. Komponent _ham_ xuddi shu xususiyatlar yoki atributlar uchun host bogʻlashlarini aniqlashi mumkin.

```angular-ts
@Component({
  ...,
  host: {
    'role': 'presentation',
    '[id]': 'id',
  }
})
export class ProfilePhoto { /* ... */ }
```

```angular-html
<profile-photo role="group" [id]="otherId" />
```

Bunday holatlarda qaysi qiymat ustun kelishini quyidagi qoidalar belgilaydi:

- Agar ikkala qiymat ham statik boʻlsa, nusxa bogʻlashi (instance binding) ustun keladi.
- Agar bir qiymat statik, ikkinchisi dinamik boʻlsa, dinamik qiymat ustun keladi.
- Agar ikkala qiymat ham dinamik boʻlsa, komponentning host bogʻlashi ustun keladi.

## CSS maxsus xususiyatlari bilan stillar berish {#styling-with-css-custom-properties}

Dasturchilar komponent stillarini moslashuvchan sozlash imkonini yaratish uchun koʻpincha [CSS maxsus xususiyatlariga](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascading_variables/Using_CSS_custom_properties) (CSS Custom Properties) tayanadi.
Bunday maxsus xususiyatlarni host elementda [stil bogʻlash](guide/templates/binding#css-style-properties) yordamida oʻrnatishingiz mumkin.

```angular-ts
@Component({
  /* ... */
  host: {
    '[style.--my-background]': 'color()',
  },
})
export class MyComponent {
  color = signal('lightgreen');
}
```

Bu misolda `--my-background` CSS maxsus xususiyati `color` signaliga bogʻlangan. `color` signali oʻzgarganda maxsus xususiyat qiymati avtomatik yangilanadi. Bu joriy komponentga va shu maxsus xususiyatga tayanadigan uning barcha bolalariga taʼsir qiladi.

### Bola komponentlarda maxsus xususiyatlarni oʻrnatish {#setting-custom-properties-on-children-components}

Shuningdek, bola komponentlarning host elementida CSS maxsus xususiyatlarini [stil bogʻlash](guide/templates/binding#css-style-properties) yordamida oʻrnatish ham mumkin.

```angular-ts
@Component({
  selector: 'my-component',
  template: `<my-child [style.--my-background]="color()" />`,
})
export class MyComponent {
  color = signal('lightgreen');
}
```

## Host element atributlarini inyeksiya qilish {#injecting-host-element-attributes}

Komponentlar va direktivalar `HostAttributeToken`'ni [`inject`](api/core/inject) funksiyasi bilan birga ishlatib, oʻz host elementidan statik atributlarni oʻqishi mumkin.

```ts
import { Component, HostAttributeToken, inject } from '@angular/core';

@Component({
  selector: 'app-button',
  ...,
})
export class Button {
  variation = inject(new HostAttributeToken('variation'));
}
```

```angular-html
<app-button variation="primary">Click me</app-button>
```

HELPFUL: Agar atribut mavjud boʻlmasa, `HostAttributeToken` xato chiqaradi, inyeksiya ixtiyoriy (optional) deb belgilangan hollar bundan mustasno.
