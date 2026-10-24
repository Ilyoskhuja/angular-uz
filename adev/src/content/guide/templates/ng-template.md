# ng-template bilan shablon fragmentlarini yaratish

[Native `<template>` elementidan](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template) ilhomlangan `<ng-template>` elementi **shablon fragmentini (template fragment)** — dinamik yoki dasturiy ravishda render qilishingiz mumkin boʻlgan kontent boʻlagini eʼlon qilish imkonini beradi.

## Shablon fragmentini yaratish {#creating-a-template-fragment}

Har qanday komponent shabloni ichida `<ng-template>` elementi bilan shablon fragmentini yaratishingiz mumkin:

```angular-html
<p>This is a normal element</p>

<ng-template>
  <p>This is a template fragment</p>
</ng-template>
```

Yuqoridagi kod render qilinganda `<ng-template>` elementining kontenti sahifada render qilinmaydi. Buning oʻrniga siz shablon fragmentiga havola olib, uni dinamik render qiladigan kod yozishingiz mumkin.

### Fragmentlar uchun bogʻlash konteksti {#binding-context-for-fragments}

Shablon fragmentlari dinamik ifodali bogʻlashlarni oʻz ichiga olishi mumkin:

```angular-ts
@Component({
  /* ... */,
  template: `<ng-template>You've selected {{count}} items.</ng-template>`,
})
export class ItemCounter {
  count: number = 0;
}
```

Shablon fragmentidagi ifoda yoki buyruqlar, fragment qayerda render qilinishidan qatʼi nazar, fragment eʼlon qilingan komponentga nisbatan hisoblanadi.

## Shablon fragmentiga havola olish {#getting-a-reference-to-a-template-fragment}

Shablon fragmentiga havolani uch usuldan birida olishingiz mumkin:

- `<ng-template>` elementida [shablon havola oʻzgaruvchisini (template reference variable)](/guide/templates/variables#template-reference-variables) eʼlon qilish orqali
- Fragmentni [komponent yoki direktiva soʻrovi](/guide/components/queries) bilan soʻrash orqali
- Toʻgʻridan-toʻgʻri `<ng-template>` elementiga qoʻllangan direktivada fragmentni inyeksiya qilish orqali.

Uchala holatda ham fragment [TemplateRef](/api/core/TemplateRef) obyekti bilan ifodalanadi.

### Shablon fragmentiga shablon havola oʻzgaruvchisi bilan murojaat qilish {#referencing-a-template-fragment-with-a-template-reference-variable}

Shu shablon faylining boshqa qismlarida shablon fragmentiga murojaat qilish uchun `<ng-template>` elementiga shablon havola oʻzgaruvchisini qoʻshishingiz mumkin:

```angular-html
<p>This is a normal element</p>

<ng-template #myFragment>
  <p>This is a template fragment</p>
</ng-template>
```

Keyin shablonning boshqa istalgan joyida `myFragment` oʻzgaruvchisi orqali bu fragmentga murojaat qilishingiz mumkin.

### Shablon fragmentiga soʻrovlar bilan murojaat qilish {#referencing-a-template-fragment-with-queries}

Har qanday [komponent yoki direktiva soʻrovi API'si](/guide/components/queries) yordamida shablon fragmentiga havola olishingiz mumkin.

`TemplateRef` obyektini `viewChild` soʻrovi yordamida toʻgʻridan-toʻgʻri soʻrashingiz mumkin.

```angular-ts
@Component({
  /* ... */,
  template: `
    <p>This is a normal element</p>

    <ng-template>
      <p>This is a template fragment</p>
    </ng-template>
  `,
})
export class ComponentWithFragment {
  templateRef = viewChild<TemplateRef<unknown>>(TemplateRef);
}
```

Keyin komponent kodingizda yoki komponent shablonida bu fragmentga boshqa har qanday klass aʼzosi kabi murojaat qilishingiz mumkin.

Agar shablonda bir nechta fragment boʻlsa, har bir `<ng-template>` elementiga shablon havola oʻzgaruvchisini qoʻshib, har bir fragmentga nom berishingiz va fragmentlarni shu nom boʻyicha soʻrashingiz mumkin:

```angular-ts
@Component({
  /* ... */,
  template: `
    <p>This is a normal element</p>

    <ng-template #fragmentOne>
      <p>This is one template fragment</p>
    </ng-template>

    <ng-template #fragmentTwo>
      <p>This is another template fragment</p>
    </ng-template>
  `,
})
export class ComponentWithFragment {
    fragmentOne = viewChild<TemplateRef<unknown>>('fragmentOne');
    fragmentTwo = viewChild<TemplateRef<unknown>>('fragmentTwo');
}
```

Yana, keyin komponent kodingizda yoki komponent shablonida bu fragmentlarga boshqa har qanday klass aʼzolari kabi murojaat qilishingiz mumkin.

### Shablon fragmentini inyeksiya qilish {#injecting-a-template-fragment}

Agar direktiva toʻgʻridan-toʻgʻri `<ng-template>` elementiga qoʻllangan boʻlsa, u `TemplateRef`'ni inyeksiya qilishi mumkin:

```angular-ts
@Directive({
  selector: '[myDirective]',
})
export class MyDirective {
  private fragment = inject(TemplateRef);
}
```

```angular-html
<ng-template myDirective>
  <p>This is one template fragment</p>
</ng-template>
```

Keyin direktiva kodingizda bu fragmentga boshqa har qanday klass aʼzosi kabi murojaat qilishingiz mumkin.

## Shablon fragmentini render qilish {#rendering-a-template-fragment}

Shablon fragmentining `TemplateRef` obyektiga havola olganingizdan soʻng, fragmentni ikki usuldan birida render qilishingiz mumkin: shablonda `NgTemplateOutlet` direktivasi bilan yoki TypeScript kodingizda `ViewContainerRef` bilan.

### `NgTemplateOutlet`'dan foydalanish {#using-ngtemplateoutlet}

`@angular/common`'dagi `NgTemplateOutlet` direktivasi `TemplateRef` qabul qiladi va fragmentni outlet joylashgan elementga **qoʻshni (sibling)** sifatida render qiladi. Odatda `NgTemplateOutlet`'ni [`<ng-container>` elementida](/guide/templates/ng-container) ishlatishingiz kerak.

Avval `NgTemplateOutlet`'ni import qiling:

```typescript
import {NgTemplateOutlet} from '@angular/common';
```

Quyidagi misol shablon fragmentini eʼlon qiladi va bu fragmentni `NgTemplateOutlet` bilan `<ng-container>` elementiga render qiladi:

```angular-html
<p>This is a normal element</p>

<ng-template #myFragment>
  <p>This is a fragment</p>
</ng-template>

<ng-container *ngTemplateOutlet="myFragment"></ng-container>
```

Bu misol quyidagi render qilingan DOM'ni hosil qiladi:

```angular-html
<p>This is a normal element</p>
<p>This is a fragment</p>
```

### `ViewContainerRef`'dan foydalanish {#using-viewcontainerref}

**View konteyneri (view container)** — Angular komponentlar daraxtidagi kontent saqlashi mumkin boʻlgan tugun. Har qanday komponent yoki direktiva oʻzining DOM'dagi joylashuviga mos view konteyneriga havola olish uchun `ViewContainerRef`'ni inyeksiya qilishi mumkin.

Shablon fragmentini dinamik render qilish uchun `ViewContainerRef`'dagi `createEmbeddedView` metodidan foydalanishingiz mumkin. Fragmentni `ViewContainerRef` bilan render qilganingizda Angular uni DOM'ga `ViewContainerRef`'ni inyeksiya qilgan komponent yoki direktivaning keyingi qoʻshnisi sifatida qoʻshadi.

Quyidagi misolda shablon fragmentiga havolani input sifatida qabul qiladigan va tugma bosilganda bu fragmentni DOM'ga render qiladigan komponent koʻrsatilgan.

```angular-ts
@Component({
  /* ... */,
  selector: 'component-with-fragment',
  template: `
    <h2>Component with a fragment</h2>
    <ng-template #myFragment>
      <p>This is the fragment</p>
    </ng-template>
    <my-outlet [fragment]="myFragment" />
  `,
})
export class ComponentWithFragment { }

@Component({
  /* ... */,
  selector: 'my-outlet',
  template: `<button (click)="showFragment()">Show</button>`,
})
export class MyOutlet {
  private viewContainer = inject(ViewContainerRef);
  fragment = input<TemplateRef<unknown> | undefined>();

  showFragment() {
    if (this.fragment()) {
      this.viewContainer.createEmbeddedView(this.fragment());
    }
  }
}
```

Yuqoridagi misolda "Show" tugmasini bosish quyidagi natijani beradi:

```angular-html
<component-with-fragment>
  <h2>Component with a fragment</h2>
  <my-outlet>
    <button>Show</button>
  </my-outlet>
  <p>This is the fragment</p>
</component-with-fragment>
```

## Shablon fragmentini render qilishda parametrlarni uzatish {#passing-parameters-when-rendering-a-template-fragment}

`<ng-template>` bilan shablon fragmentini eʼlon qilganda, qoʻshimcha ravishda fragment qabul qiladigan parametrlarni ham eʼlon qilishingiz mumkin. Fragmentni render qilganda ixtiyoriy ravishda shu parametrlarga mos `context` obyektini uzatishingiz mumkin. Bogʻlash ifodalari va buyruqlarida, fragment eʼlon qilingan komponentning maʼlumotlariga murojaat qilishdan tashqari, shu kontekst obyektidagi maʼlumotlardan ham foydalanishingiz mumkin.

Har bir parametr `let-` prefiksli atribut sifatida yoziladi va uning qiymati kontekst obyektidagi xususiyat nomiga mos keladi:

```angular-html
<ng-template let-pizzaTopping="topping">
  <p>You selected: {{ pizzaTopping }}</p>
</ng-template>
```

### `NgTemplateOutlet`'dan foydalanish {#using-ngtemplateoutlet-with-parameters}

Kontekst obyektini `ngTemplateOutletContext` input'iga bogʻlashingiz mumkin:

```angular-html
<ng-template #myFragment let-pizzaTopping="topping">
  <p>You selected: {{ pizzaTopping }}</p>
</ng-template>

<ng-container [ngTemplateOutlet]="myFragment" [ngTemplateOutletContext]="{topping: 'onion'}" />
```

### `ViewContainerRef`'dan foydalanish {#using-viewcontainerref-with-parameters}

Kontekst obyektini `createEmbeddedView`'ga ikkinchi argument sifatida uzatishingiz mumkin:

```ts
this.viewContainer.createEmbeddedView(this.myFragment, {topping: 'onion'});
```

## Shablon fragmentlariga injector'lar berish {#providing-injectors-to-template-fragments}

Shablon fragmentini render qilganingizda uning injector konteksti render qilingan joydan emas, balki **shablon eʼlon qilingan joydan** olinadi. Maxsus injector berish orqali bu xatti-harakatni oʻzgartirishingiz mumkin.

### `NgTemplateOutlet`'dan foydalanish {#using-ngtemplateoutlet-with-injectors}

Maxsus `Injector`'ni `ngTemplateOutletInjector` input'iga uzatishingiz mumkin:

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
  selector: 'root',
  imports: [NgTemplateOutlet, ThemedPanel],
  template: `
    <ng-template #myFragment>
      <themed-panel />
    </ng-template>
    <ng-container *ngTemplateOutlet="myFragment; injector: customInjector" />
  `,
})
export class Root {
  customInjector = Injector.create({
    providers: [{provide: THEME_DATA, useValue: 'dark'}],
  });
}
```

#### Outlet'ning injector'ini meros qilib olish {#inheriting-the-outlets-injector}

Joylashtirilgan view (embedded view) oʻz injector'ini shablon eʼlon qilingan joydan emas, balki outlet'ning DOM'dagi joylashuvidan meros qilib olishi uchun `ngTemplateOutletInjector`'ga `'outlet'` satrini oʻrnatishingiz mumkin.

```angular-html
<ng-template #node let-items>
  <item-component>
    @for (child of items; track $index) {
      <ng-container
        *ngTemplateOutlet="node; context: {$implicit: child.children}; injector: 'outlet'"
      />
    }
  </item-component>
</ng-template>

<ng-container *ngTemplateOutlet="node; context: {$implicit: topLevelItems}" />
```

`node` shablonining har bir rekursiv render qilinishi injector'ni oʻrab turgan `<item-component>`'dan meros qilib oladi; bu har bir ichki darajaga oʻz ota komponentiga tegishli provider'larga murojaat qilish imkonini beradi.

NOTE: Bu rekursiv strukturalarni yaratishda yoki render qilinadigan shablon outlet joylashgan joydagi komponentlar daraxtidan provider'larga murojaat qilishi kerak boʻlgan har qanday holatda foydalidir.

### `ViewContainerRef`'dan foydalanish {#using-viewcontainerref-with-injectors}

Maxsus injector'ni `createEmbeddedView`'dagi parametrlar (options) obyektining bir qismi sifatida uzatishingiz mumkin:

```ts
this.viewContainer.createEmbeddedView(this.myFragment, context, {
  injector: myCustomInjector,
});
```

## Strukturaviy direktivalar {#structural-directives}

**Strukturaviy direktiva (structural directive)** — quyidagilarni bajaradigan har qanday direktiva:

- `TemplateRef`'ni inyeksiya qiladi
- `ViewContainerRef`'ni inyeksiya qiladi va inyeksiya qilingan `TemplateRef`'ni dasturiy ravishda render qiladi

Angular strukturaviy direktivalar uchun maxsus qulay sintaksisni qoʻllab-quvvatlaydi. Agar direktivani elementga qoʻllasangiz va direktiva selektorining oldiga yulduzcha (`*`) belgisini qoʻysangiz, Angular butun elementni va uning barcha kontentini shablon fragmenti sifatida qabul qiladi:

```angular-html
<section *myDirective>
  <p>This is a fragment</p>
</section>
```

Bu quyidagiga tengdir:

```angular-html
<ng-template myDirective>
  <section>
    <p>This is a fragment</p>
  </section>
</ng-template>
```

Dasturchilar odatda strukturaviy direktivalardan fragmentlarni shartli render qilish yoki fragmentlarni bir necha marta render qilish uchun foydalanadilar.

Batafsil maʼlumot uchun [Strukturaviy direktivalar](/guide/directives/structural-directives) boʻlimiga qarang.

## Qoʻshimcha manbalar {#additional-resources}

`ng-template`'ning boshqa kutubxonalarda qanday ishlatilishiga misollar uchun quyidagilarga qarang:

- [Angular Material'dagi Tabs](https://material.angular.dev/components/tabs/overview) - tab faollashtirilmaguncha DOM'ga hech narsa render qilinmaydi
- [Angular Material'dagi Table](https://material.angular.dev/components/table/overview) - dasturchilarga maʼlumotlarni render qilishning turli usullarini aniqlash imkonini beradi
