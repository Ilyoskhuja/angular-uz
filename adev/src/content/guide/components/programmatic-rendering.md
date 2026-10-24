# Komponentlarni programmatik tarzda render qilish

TIP: Bu qoʻllanma siz [Asosiy tushunchalar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Komponentni shablonda bevosita ishlatishdan tashqari, komponentlarni programmatik tarzda dinamik render qilishingiz ham mumkin. Bu komponent dastlab nomaʼlum boʻlgan (shu sababli shablonda unga bevosita murojaat qilib boʻlmaydigan) va qandaydir shartlarga bogʻliq boʻlgan holatlarda foydalidir.

Komponentni programmatik tarzda render qilishning ikkita asosiy usuli mavjud: shablonda `NgComponentOutlet` yordamida yoki TypeScript kodingizda `ViewContainerRef` yordamida.

HELPFUL: lazy loading holatlari uchun (masalan, ogʻir komponentning yuklanishini kechiktirmoqchi boʻlsangiz) oʻrniga oʻrnatilgan [`@defer` imkoniyatidan](/guide/templates/defer) foydalanishni koʻrib chiqing. `@defer` imkoniyati `@defer` bloki ichidagi istalgan komponentlar, direktivalar va pipe'lar kodini avtomatik ravishda alohida JavaScript chunk'lariga ajratib olish va sozlangan trigger'lar asosida faqat zarur boʻlganda yuklash imkonini beradi.

## NgComponentOutlet'dan foydalanish {#using-ngcomponentoutlet}

`NgComponentOutlet` — berilgan komponentni shablonda dinamik render qiladigan strukturaviy direktiva.

```angular-ts
import {NgComponentOutlet} from '@angular/common';

@Component({/*...*/})
export class AdminBio {
  /* ... */
}

@Component({/*...*/})
export class StandardBio {
  /* ... */
}

@Component({
  imports: [NgComponentOutlet],
  template: `
    <p>Profile for {{ user().name }}</p>
    <ng-container *ngComponentOutlet="bioComponent()" />
  `,
})
export class CustomDialog {
  user = input.required<User>();

  bioComponent = computed(() => {
    return this.user().isAdmin ? AdminBio : StandardBio;
  });
}
```

### Dinamik render qilingan komponentlarga input'larni uzatish {#passing-inputs-to-dynamically-rendered-components}

`ngComponentOutletInputs` xususiyati yordamida dinamik render qilingan komponentga input'larni uzatishingiz mumkin. Bu xususiyat kalitlari input nomlari, qiymatlari esa input qiymatlari boʻlgan obyektni qabul qiladi.

```angular-ts
@Component({
  selector: 'user-greeting',
  template: `
    <div>
      <p>User: {{ username() }}</p>
      <p>Role: {{ role() }}</p>
    </div>
  `,
})
export class UserGreeting {
  username = input.required<string>();
  role = input('guest');
}

@Component({
  selector: 'profile-view',
  imports: [NgComponentOutlet],
  template: `<ng-container *ngComponentOutlet="greetingComponent; inputs: greetingInputs()" />`,
})
export class ProfileView {
  greetingComponent = UserGreeting;
  greetingInputs = signal({username: 'ngAwesome', role: 'admin'});
}
```

`greetingInputs` signali oʻzgargan har safar input'lar yangilanadi va dinamik komponent ota komponentning holati bilan sinxron saqlanadi.

### Kontent proyeksiyasini taqdim etish {#providing-content-projection}

Dinamik render qilingan komponentga proyeksiya qilingan kontentni uzatish uchun `ngComponentOutletContent`'dan foydalaning. Bu dinamik komponent kontentni koʻrsatish uchun `<ng-content>`'dan foydalanganda qoʻl keladi.

```angular-ts
@Component({
  selector: 'card-wrapper',
  template: `
    <div class="card">
      <ng-content />
    </div>
  `,
})
export class CardWrapper {}

@Component({
  imports: [NgComponentOutlet],
  template: `
    <ng-container *ngComponentOutlet="cardComponent; content: cardContent()" />

    <ng-template #contentTemplate>
      <h3>Dynamic Content</h3>
      <p>This content is projected into the card.</p>
    </ng-template>
  `,
})
export class DynamicCard {
  private vcr = inject(ViewContainerRef);
  cardComponent = CardWrapper;

  private contentTemplate = viewChild<TemplateRef<unknown>>('contentTemplate');

  cardContent = computed(() => {
    const template = this.contentTemplate();
    if (!template) return [];
    // Returns an array of projection slots. Each element represents one <ng-content> slot.
    // CardWrapper has one <ng-content>, so we return an array with one element.
    return [this.vcr.createEmbeddedView(template).rootNodes];
  });
}
```

NOTE: Gidratsiya native DOM API'lari yordamida yaratilgan DOM tugunlarini proyeksiya qilishni qoʻllab-quvvatlamaydi. Bu [NG0503 xatosiga](/errors/NG0503) olib keladi. Proyeksiya qilinadigan kontentni yaratish uchun Angular API'laridan foydalaning yoki komponentga `ngSkipHydration` qoʻshing.

### Injector'larni taqdim etish {#providing-injectors}

`ngComponentOutletInjector` yordamida dinamik yaratilgan komponentga maxsus injector taqdim etishingiz mumkin. Bu komponentga xos servislar yoki konfiguratsiyani taqdim etish uchun foydalidir.

```angular-ts
export const THEME_DATA = new InjectionToken<string>('THEME_DATA', {
  factory: () => 'light',
});

@Component({
  selector: 'themed-panel',
  template: `<div [class]="theme">...</div>`,
})
export class ThemedPanel {
  theme = inject(THEME_DATA);
}

@Component({
  selector: 'dynamic-panel',
  imports: [NgComponentOutlet],
  template: `<ng-container *ngComponentOutlet="panelComponent; injector: customInjector" />`,
})
export class DynamicPanel {
  panelComponent = ThemedPanel;

  customInjector = Injector.create({
    providers: [{provide: THEME_DATA, useValue: 'dark'}],
  });
}
```

### Komponent nusxasiga murojaat qilish {#accessing-the-component-instance}

Direktivaning `exportAs` imkoniyati yordamida dinamik yaratilgan komponentning nusxasiga murojaat qilishingiz mumkin:

```angular-ts
@Component({
  selector: 'counter',
  template: `<p>Count: {{ count() }}</p>`,
})
export class Counter {
  count = signal(0);
  increment() {
    this.count.update((c) => c + 1);
  }
}

@Component({
  imports: [NgComponentOutlet],
  template: `
    <ng-container [ngComponentOutlet]="counterComponent" #outlet="ngComponentOutlet" />

    <button (click)="outlet.componentInstance?.increment()">Increment</button>
  `,
})
export class CounterHost {
  counterComponent = Counter;
}
```

NOTE: Komponent render qilinishidan oldin `componentInstance` xususiyati `null` boʻladi.

Direktivaning imkoniyatlari haqida koʻproq maʼlumot olish uchun [NgComponentOutlet API maʼlumotnomasiga](api/common/NgComponentOutlet) qarang.

## ViewContainerRef'dan foydalanish {#using-viewcontainerref}

**View konteyneri** — Angular komponent daraxtidagi kontent saqlashi mumkin boʻlgan tugun. Har qanday komponent yoki direktiva oʻsha komponent yoki direktivaning DOM'dagi joylashuviga mos keluvchi view konteyneriga havola olish uchun `ViewContainerRef`'ni inyeksiya qilishi mumkin.

Komponentni dinamik yaratish va render qilish uchun `ViewContainerRef`'dagi `createComponent` metodidan foydalanishingiz mumkin. `ViewContainerRef` yordamida yangi komponent yaratganingizda Angular uni DOM'ga `ViewContainerRef`'ni inyeksiya qilgan komponent yoki direktivaning keyingi qoʻshni elementi sifatida qoʻshadi.

```angular-ts
@Component({
  selector: 'leaf-content',
  template: `This is the leaf content`,
})
export class LeafContent {}

@Component({
  selector: 'outer-container',
  template: `
    <p>This is the start of the outer container</p>
    <inner-item />
    <p>This is the end of the outer container</p>
  `,
})
export class OuterContainer {}

@Component({
  selector: 'inner-item',
  template: `<button (click)="loadContent()">Load content</button>`,
})
export class InnerItem {
  private viewContainer = inject(ViewContainerRef);

  loadContent() {
    this.viewContainer.createComponent(LeafContent);
  }
}
```

Yuqoridagi misolda "Load content" tugmasini bosish quyidagi DOM tuzilmasiga olib keladi

```angular-html
<outer-container>
  <p>This is the start of the outer container</p>
  <inner-item>
    <button>Load content</button>
  </inner-item>
  <leaf-content>This is the leaf content</leaf-content>
  <p>This is the end of the outer container</p>
</outer-container>
```

## Komponentlarni lazy loading qilish {#lazy-loading-components}

HELPFUL: agar baʼzi komponentlarni lazy loading (kechiktirilgan yuklash) qilmoqchi boʻlsangiz, oʻrniga oʻrnatilgan [`@defer` imkoniyatidan](/guide/templates/defer) foydalanishni koʻrib chiqishingiz mumkin.

Agar sizning holatingiz `@defer` imkoniyati bilan qamrab olinmasa, `NgComponentOutlet` yoki `ViewContainerRef`'ni standart JavaScript [dinamik import](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/import) bilan birga ishlatishingiz mumkin.

```angular-ts
@Component({
  ...,
  template: `
    <section>
      <h2>Basic settings</h2>
      <basic-settings />
    </section>
    <section>
      <h2>Advanced settings</h2>
      @if(!advancedSettings) {
        <button (click)="loadAdvanced()">
          Load advanced settings
        </button>
      }
      <ng-container *ngComponentOutlet="advancedSettings" />
    </section>
  `
})
export class AdminSettings {
  advancedSettings: {new(): AdvancedSettings} | undefined;

  async loadAdvanced() {
    const { AdvancedSettings } = await import('path/to/advanced_settings.js');
    this.advancedSettings = AdvancedSettings;
  }
}
```

Yuqoridagi misol tugma bosilganda `AdvancedSettings`'ni yuklaydi va koʻrsatadi.

## Yaratish vaqtida input'lar, output'larni bogʻlash va host direktivalarini oʻrnatish {#binding-inputs-outputs-and-setting-host-directives-at-creation}

Komponentlarni dinamik yaratishda input'larni qoʻlda oʻrnatish va output'larga obuna boʻlish xatolarga moyil boʻlishi mumkin. Komponent nusxasi yaratilgandan keyin bogʻlashlarni ulash uchun koʻpincha qoʻshimcha kod yozishingiz kerak boʻladi.

Buni soddalashtirish uchun `createComponent` ham, `ViewContainerRef.createComponent` ham input'lar va output'larni oldindan sozlash uchun `inputBinding()`, `outputBinding()` va `twoWayBinding()` kabi yordamchilardan iborat `bindings` massivini uzatishni qoʻllab-quvvatlaydi. Shuningdek, istalgan host direktivalarini qoʻllash uchun `directives` massivini ham koʻrsatishingiz mumkin. Bu komponentlarni shablondagiga oʻxshash bogʻlashlar bilan yagona deklarativ chaqiruvda programmatik tarzda yaratish imkonini beradi.

### `ViewContainerRef.createComponent` yordamida host view {#host-view-using-viewcontainerrefcreatecomponent}

`ViewContainerRef.createComponent` komponent yaratadi va uning host view'i hamda host elementini konteyner joylashgan oʻringa, konteynerning view ierarxiyasiga avtomatik joylashtiradi. Dinamik komponent konteynerning mantiqiy va vizual tuzilmasining bir qismiga aylanishi kerak boʻlganda (masalan, roʻyxat elementlari yoki inline UI qoʻshishda) shundan foydalaning.

Bundan farqli oʻlaroq, mustaqil `createComponent` API'si yangi komponentni hech qanday mavjud view yoki DOM joylashuviga biriktirmaydi — u `ComponentRef` qaytaradi va komponentning host elementini qayerga joylashtirishni aniq nazorat qilish imkonini beradi.

```angular-ts
import {Component, input, model, output} from '@angular/core';

@Component({
  selector: 'app-warning',
  template: `
    @if (isExpanded()) {
      <section>
        <p>Warning: Action needed!</p>
        <button (click)="close.emit(true)">Close</button>
      </section>
    }
  `,
})
export class AppWarning {
  readonly canClose = input.required<boolean>();
  readonly isExpanded = model<boolean>();
  readonly close = output<boolean>();
}
```

```ts
import {
  Component,
  ViewContainerRef,
  signal,
  inputBinding,
  outputBinding,
  twoWayBinding,
  inject,
} from '@angular/core';
import {FocusTrap} from '@angular/cdk/a11y';
import {ThemeDirective} from '../theme.directive';

@Component({
  template: `<ng-container #container />`,
})
export class Host {
  private vcr = inject(ViewContainerRef);
  readonly canClose = signal(true);
  readonly isExpanded = signal(true);

  showWarning() {
    const compRef = this.vcr.createComponent(AppWarning, {
      bindings: [
        inputBinding('canClose', this.canClose),
        twoWayBinding('isExpanded', this.isExpanded),
        outputBinding<boolean>('close', (confirmed) => {
          console.log('Closed with result:', confirmed);
        }),
      ],
      directives: [
        FocusTrap,
        {type: ThemeDirective, bindings: [inputBinding('theme', () => 'warning')]},
      ],
    });
  }
}
```

Yuqoridagi misolda dinamik **AppWarning** komponenti `canClose` input'i reaktiv signalga bogʻlangan, `isExpanded` holatida ikki tomonlama bogʻlash va `close` uchun output tinglovchisi bilan yaratiladi. `FocusTrap` va `ThemeDirective` host elementga `directives` orqali biriktiriladi.

### `createComponent` + `hostElement` yordamida `document.body`'ga biriktirilgan popup {#popup-attached-to-documentbody-with-createcomponent--hostelement}

Joriy view ierarxiyasidan tashqarida render qilishda (masalan, overlay'lar) shundan foydalaning. Berilgan `hostElement` DOM'da komponentning host'iga aylanadi, shu sababli Angular selektorga mos yangi element yaratmaydi. **Bogʻlashlarni** bevosita sozlash imkonini beradi.

```ts
import {
  ApplicationRef,
  createComponent,
  EnvironmentInjector,
  inject,
  Injectable,
  inputBinding,
  outputBinding,
  Service,
} from '@angular/core';
import {Popup} from './popup';

@Service()
export class PopupService {
  private readonly injector = inject(EnvironmentInjector);
  private readonly appRef = inject(ApplicationRef);

  show(message: string) {
    // Create a host element for the popup
    const host = document.createElement('popup-host');

    // Create the component and bind in one call
    const ref = createComponent(Popup, {
      environmentInjector: this.injector,
      hostElement: host,
      bindings: [
        inputBinding('message', () => message),
        outputBinding('closed', () => {
          document.body.removeChild(host);
          this.appRef.detachView(ref.hostView);
          ref.destroy();
        }),
      ],
    });

    // Registers the component’s view so it participates in change detection cycle.
    this.appRef.attachView(ref.hostView);
    // Inserts the provided host element into the DOM (outside the normal Angular view hierarchy).
    // This is what makes the popup visible on screen, typically used for overlays or modals.
    document.body.appendChild(host);
  }
}
```

## Render qilish xatolariga ishlov berish {#handling-rendering-errors}

`ViewContainerRef.createComponent` yoki mustaqil `createComponent` funksiyasi yordamida komponentlarni dinamik yaratishda, render qilish yoki oʻzgarishlarni aniqlash bosqichlarida yuzaga keladigan xatolarga ishlov berish uchun opsiyalar obyektida `onError` callback'ini taqdim etishingiz mumkin. Bu shablonlardagi `@error` blokidan foydalanishning programmatik ekvivalentidir.

```ts
viewContainerRef.createComponent(DynamicComponent, {
  onError: (err: Error, details: ErrorDetails) => {
    console.error('Component rendering failed:', err);
    // Render an alternative UI or log metrics
  },
});
```

NOTE: `onError` callback'i faqat render qilish yoki oʻzgarishlarni aniqlash bosqichlarida yuzaga keladigan xatolarni ushlaydi. U komponent nusxasini yaratish vaqtida (masalan, konstruktorda) yuzaga keladigan xatolarni ushlamaydi. Angular API'ni chaqirganingizda yaratish xatolarini sinxron tarzda tashlaydi.
