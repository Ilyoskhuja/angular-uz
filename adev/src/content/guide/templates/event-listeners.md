# Hodisa tinglovchilarini qoʻshish

Angular shablondagi elementda hodisa tinglovchilarini (event listener) aniqlashni qoʻllab-quvvatlaydi: bunda hodisa nomi qavs ichida, hodisa har safar yuz berganda bajariladigan ifoda bilan birga koʻrsatiladi.

## Native hodisalarni tinglash {#listening-to-native-events}

HTML elementiga hodisa tinglovchilarini qoʻshmoqchi boʻlsangiz, hodisani qavslar `()` ichiga olasiz; bu tinglovchi ifodasini koʻrsatish imkonini beradi.

```angular-ts
@Component({
  template: `
    <input type="text" (keyup)="updateField()" />
  `,
  ...
})
export class App{
  updateField(): void {
    console.log('Field is updated!');
  }
}
```

Bu misolda `<input>` elementi har safar `keyup` hodisasini yuborganda Angular `updateField`'ni chaqiradi.

Har qanday native hodisalar uchun tinglovchi qoʻshishingiz mumkin, masalan: `click`, `keydown`, `mouseover` va boshqalar. Koʻproq bilish uchun [MDN'dagi elementlarda mavjud barcha hodisalar](https://developer.mozilla.org/en-US/docs/Web/API/Element#events) roʻyxatiga qarang.

## Hodisa argumentiga murojaat qilish {#accessing-the-event-argument}

Har bir shablon hodisa tinglovchisida Angular hodisa obyektiga havolani oʻz ichiga olgan `$event` nomli oʻzgaruvchini taqdim etadi.

```angular-ts
@Component({
  template: `
    <input type="text" (keyup)="updateField($event)" />
  `,
  ...
})
export class App {
  updateField(event: KeyboardEvent): void {
    console.log(`The user pressed: ${event.key}`);
  }
}
```

## Tugma modifikatorlaridan foydalanish {#using-key-modifiers}

Maʼlum bir tugma uchun maʼlum klaviatura hodisalarini ushlamoqchi boʻlsangiz, quyidagiga oʻxshash kod yozishingiz mumkin:

```angular-ts
@Component({
  template: `
    <input type="text" (keyup)="updateField($event)" />
  `,
  ...
})
export class App {
  updateField(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      console.log('The user pressed enter in the text field.');
    }
  }
}
```

Biroq bu keng tarqalgan holat boʻlgani uchun Angular nuqta (`.`) belgisi orqali maʼlum tugmani koʻrsatib, hodisalarni filtrlash imkonini beradi. Shu yoʻl bilan kodni quyidagicha soddalashtirish mumkin:

```angular-ts
@Component({
  template: `
    <input type="text" (keyup.enter)="updateField($event)" />
  `,
  ...
})
export class App{
  updateField(event: KeyboardEvent): void {
    console.log('The user pressed enter in the text field.');
  }
}
```

Qoʻshimcha tugma modifikatorlarini ham qoʻshishingiz mumkin:

```angular-html
<!-- Matches shift and enter -->
<input type="text" (keyup.shift.enter)="updateField($event)" />
```

Angular `alt`, `control`, `meta` va `shift` modifikatorlarini qoʻllab-quvvatlaydi.

Klaviatura hodisalariga bogʻlamoqchi boʻlgan tugmani (key) yoki kodni (code) koʻrsatishingiz mumkin. Key va code maydonlari brauzerning klaviatura hodisasi obyektining native qismidir. Sukut boʻyicha hodisa bogʻlashi siz [klaviatura hodisalari uchun Key qiymatlaridan](https://developer.mozilla.org/docs/Web/API/UI_Events/Keyboard_event_key_values) foydalanmoqchi deb hisoblaydi.

Angular shuningdek oʻrnatilgan `code` suffiksi orqali [klaviatura hodisalari uchun Code qiymatlarini](https://developer.mozilla.org/docs/Web/API/UI_Events/Keyboard_event_code_values) koʻrsatish imkonini ham beradi.

```angular-html
<!-- Matches alt and left shift -->
<input type="text" (keydown.code.alt.shiftleft)="updateField($event)" />
```

Bu turli operatsion tizimlarda klaviatura hodisalariga bir xil tarzda ishlov berish uchun foydali boʻlishi mumkin. Masalan, macOS qurilmalarida Alt tugmasi ishlatilganda `key` xususiyati tugmani Alt tugmasi tomonidan allaqachon oʻzgartirilgan belgi asosida qaytaradi. Bu Alt + S kabi kombinatsiya `key` qiymati sifatida `'ß'` qaytarishini anglatadi. `code` xususiyati esa hosil boʻlgan belgiga emas, balki bosilgan jismoniy yoki virtual tugmaga mos keladi.

## Global maqsadlarda tinglash {#listening-on-global-targets}

Hodisaga prefiks sifatida global maqsad (target) nomlaridan foydalanish mumkin. Qoʻllab-quvvatlanadigan 3 ta global maqsad: `window`, `document` va `body`.

```angular-ts
@Component({
  /* ... */
  host: {
    '(window:click)': 'onWindowClick()',
    '(document:click)': 'onDocumentClick()',
    '(body:click)': 'onBodyClick()',
  },
})
export class MyView {}
```

## Hodisaning sukut boʻyicha xatti-harakatini oldini olish {#preventing-event-default-behavior}

Agar hodisa ishlov beruvchingiz brauzerning native xatti-harakatini almashtirishi kerak boʻlsa, hodisa obyektining [`preventDefault` metodidan](https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault) foydalanishingiz mumkin:

```angular-ts
@Component({
  template: `
    <a href="#overlay" (click)="showOverlay($event)">
  `,
  ...
})
export class App{
  showOverlay(event: PointerEvent): void {
    event.preventDefault();
    console.log('Show overlay without updating the URL!');
  }
}
```

Agar hodisa ishlov beruvchisi ifodasining qiymati `false` boʻlsa, Angular [native hodisa ishlov beruvchi atributlariga](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes#event_handler_attributes) oʻxshab `preventDefault()`'ni avtomatik chaqiradi. _Doimo `preventDefault`'ni aniq chaqirishni afzal koʻring_, chunki bu yondashuv kodning maqsadini ravshan qiladi.

## Hodisalarga ishlov berishni kengaytirish {#extend-event-handling}

Angular'ning hodisa tizimi `EVENT_MANAGER_PLUGINS` inyeksiya tokeni bilan roʻyxatdan oʻtkazilgan maxsus hodisa plaginlari orqali kengaytirilishi mumkin.

### Hodisa plaginini amalga oshirish {#implementing-event-plugin}

Maxsus hodisa plaginini yaratish uchun `EventManagerPlugin` klassini kengaytiring va talab qilinadigan metodlarni amalga oshiring.

```ts
import {Injectable} from '@angular/core';
import {EventManagerPlugin} from '@angular/platform-browser';

@Injectable()
export class DebounceEventPlugin extends EventManagerPlugin {
  constructor() {
    super(document);
  }

  // Define which events this plugin supports
  override supports(eventName: string) {
    return /debounce/.test(eventName);
  }

  // Handle the event registration
  override addEventListener(element: HTMLElement, eventName: string, handler: Function) {
    // Parse the event: e.g., "click.debounce.500"
    // event: "click", delay: 500
    const [event, , delay = '300'] = eventName.split('.');

    let timeoutId: ReturnType<typeof setTimeout>;

    const listener = (e: Event) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        handler(e);
      }, Number(delay));
    };

    element.addEventListener(event, listener);

    // Return cleanup function
    return () => {
      clearTimeout(timeoutId);
      element.removeEventListener(event, listener);
    };
  }
}
```

Maxsus plaginingizni ilovangiz provider'larida `EVENT_MANAGER_PLUGINS` tokeni yordamida roʻyxatdan oʻtkazing:

```ts
import {bootstrapApplication, EVENT_MANAGER_PLUGINS} from '@angular/platform-browser';
import {App} from './app';
import {DebounceEventPlugin} from './debounce-event-plugin';

bootstrapApplication(App, {
  providers: [
    {
      provide: EVENT_MANAGER_PLUGINS,
      useClass: DebounceEventPlugin,
      multi: true,
    },
  ],
});
```

Roʻyxatdan oʻtkazilgandan soʻng maxsus hodisa sintaksisingizni shablonlarda, shuningdek `host` xususiyati bilan ham ishlatishingiz mumkin:

```angular-ts
@Component({
  template: `
    <input
      type="text"
      (input.debounce.500)="onSearch($event.target.value)"
      placeholder="Search..."
    />
  `,
  ...
})
export class Search {
 onSearch(query: string): void {
    console.log('Searching for:', query);
  }
}
```

```ts
@Component({
  ...,
  host: {
    '(click.debounce.500)': 'handleDebouncedClick()',
  },
})
export class AwesomeCard {
  handleDebouncedClick(): void {
   console.log('Debounced click!');
  }
}
```
