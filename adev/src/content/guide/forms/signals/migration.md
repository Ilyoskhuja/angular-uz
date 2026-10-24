# Mavjud formalarni Signal Forms'ga migratsiya qilish

Ushbu qoʻllanma mavjud kod bazalarini Signal Forms'ga migratsiya qilish strategiyalarini taqdim etadi va mavjud
reaktiv formalar (Reactive Forms) bilan oʻzaro moslikka (interoperability) eʼtibor qaratadi.

## `compatForm` yordamida yuqoridan pastga migratsiya {#top-down-migration-using-compatform}

Baʼzan Signal Form ichida mavjud reaktiv `FormControl` nusxalaridan foydalanishni istashingiz mumkin. Bu quyidagilarni oʻz ichiga olgan
kontrollar uchun foydali:

- Murakkab asinxron logika.
- Hali koʻchirilmagan (port qilinmagan) murakkab RxJS operatorlari.
- Mavjud uchinchi tomon kutubxonalari bilan integratsiya.

### `FormControl`'ni signal formaga integratsiya qilish {#integrating-a-formcontrol-into-a-signal-form}

Maxsus `enterprisePasswordValidator`'dan foydalanadigan mavjud `passwordControl`'ni koʻrib chiqaylik. Validatorni qayta yozish oʻrniga,
kontrolni signal holatingizga koʻprik orqali ulashingiz mumkin.

Buni `compatForm` yordamida qilishimiz mumkin:

```typescript
import {signal} from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import {compatForm} from '@angular/forms/signals/compat';

// 1. Existing control with a specialized validator
const passwordControl = new FormControl('', {
  validators: [Validators.required, enterprisePasswordValidator()],
  nonNullable: true,
});

// 2. Wrap it inside your form state signal
const user = signal({
  email: '',
  password: passwordControl, // Nest the existing control directly
});

// 3. Create the form
const f = compatForm(user);

// Access values via the signal tree
console.log(f.email().value()); // Current email value
console.log(f.password().value()); // Current value of passwordControl

// Reactive state is proxied automatically
const isPasswordValid = f.password().valid();
const passwordErrors = f.password().errors(); // Returns CompatValidationError if the existing validator fails
```

Shablonda asosiy kontrolni bogʻlab, standart reaktiv sintaksisdan foydalaning:

```angular-html
<form novalidate>
  <div>
    <label>
      Email:
      <input [formField]="f.email" />
    </label>
  </div>

  <div>
    <label>
      Password:
      <input [formField]="f.password" type="password" />
    </label>

    @if (f.password().touched() && f.password().invalid()) {
      <div class="error-list">
        @for (error of f.password().errors(); track error) {
          <p>{{ error.message || error.kind }}</p>
        }
      </div>
    }
  </div>
</form>
```

<docs-code-multifile preview path="adev/src/content/examples/signal-forms/src/compat-form-control-integration/app/app.ts">
  <docs-code header="app.ts" path="adev/src/content/examples/signal-forms/src/compat-form-control-integration/app/app.ts"/>
  <docs-code header="app.html" path="adev/src/content/examples/signal-forms/src/compat-form-control-integration/app/app.html"/>
</docs-code-multifile>

### `FormGroup`'ni signal formaga integratsiya qilish {#integrating-a-formgroup-into-a-signal-form}

Butun `FormGroup`'ni ham oʻrashingiz mumkin. Bu formaning qayta ishlatiladigan kichik boʻlimi — masalan,
**Manzil bloki** — hali ham mavjud reaktiv formalar tomonidan boshqarilayotgan holatlarda keng tarqalgan.

```typescript
import {signal} from '@angular/core';
import {FormGroup, FormControl, Validators} from '@angular/forms';
import {compatForm} from '@angular/forms/signals/compat';

// 1. An existing address group with its own validation logic
const addressGroup = new FormGroup({
  street: new FormControl('123 Angular Way', Validators.required),
  city: new FormControl('Mountain View', Validators.required),
  zip: new FormControl('94043', Validators.required),
});

// 2. Include it in the state like it's a value
const checkoutModel = signal({
  customerName: 'Pirojok the Cat',
  shippingAddress: addressGroup,
});

const f = compatForm(checkoutModel, (p) => {
  required(p.customerName);
});
```

`shippingAddress` maydoni Signal Form daraxtingizda shox (branch) vazifasini bajaradi. Ushbu ichki kontrollarni shablonda
`.control()` orqali asosiy mavjud kontrollarga murojaat qilib bogʻlashingiz mumkin:

```angular-html
<form novalidate>
  <h3>Shipping Details</h3>

  <div>
    <label>
      Customer Name:
      <input [formField]="f.customerName" />
    </label>

    @if (f.customerName().touched() && f.customerName().invalid()) {
      <div class="error-list">
        <p>Customer name is required.</p>
      </div>
    }
  </div>

  <fieldset>
    <legend>Address</legend>

    @let street = f.shippingAddress().control().controls.street;
    <div>
      <label>
        Street:
        <input [formControl]="street" />
      </label>
      @if (street.touched && street.invalid) {
        <div class="error-list">
          <p>Street is required</p>
        </div>
      }
    </div>

    @let city = f.shippingAddress().control().controls.city;
    <div>
      <label>
        City:
        <input [formControl]="city" />
      </label>
      @if (city.touched && city.invalid) {
        <div class="error-list">
          <p>City is required</p>
        </div>
      }
    </div>

    @let zip = f.shippingAddress().control().controls.zip;
    <div>
      <label>
        Zip Code:
        <input [formControl]="zip" />
      </label>
      @if (zip.touched && zip.invalid) {
        <div class="error-list">
          <p>Zip Code is required</p>
        </div>
      }
    </div>
  </fieldset>
</form>
```

<docs-code-multifile preview path="adev/src/content/examples/signal-forms/src/compat-form-group-integration/app/app.ts">
  <docs-code header="app.ts" path="adev/src/content/examples/signal-forms/src/compat-form-group-integration/app/app.ts"/>
  <docs-code header="app.html" path="adev/src/content/examples/signal-forms/src/compat-form-group-integration/app/app.html"/>
</docs-code-multifile>

### Qiymatlarga murojaat qilish {#accessing-values}

`compatForm` qiymatga murojaatni `FormControl` darajasida proksilasa-da, formaning toʻliq qiymati kontrolni saqlab qoladi:

```typescript
const passwordControl = new FormControl('password' /** ... */);

const user = signal({
  email: '',
  password: passwordControl, // Nest the existing control directly
});

const form = compatForm(user);
form.password().value(); // 'password'
form().value(); // { email: '', password: FormControl}
```

Agar sizga formaning butun qiymati kerak boʻlsa, uni qoʻlda tuzishingiz kerak boʻladi:

```typescript
const formValue = computed(() => ({
  email: form.email().value(),
  password: form.password().value(),
})); // {email: '', password: ''}
```

## Pastdan yuqoriga migratsiya {#bottom-up-migration}

### Signal Form'ni `FormGroup`'ga integratsiya qilish {#integrating-a-signal-form-into-a-formgroup}

Signallarga asoslangan formani standart `FormControl` sifatida taqdim etish uchun `SignalFormControl`'dan foydalanishingiz mumkin. Bu ota `FormGroup` tuzilmasini
saqlab qolgan holda formaning barg tugunlarini (leaf nodes) signallarga migratsiya qilmoqchi boʻlganingizda foydali.

```typescript
import {Component, signal} from '@angular/core';
import {ReactiveFormsModule, FormGroup} from '@angular/forms';
import {SignalFormControl} from '@angular/forms/signals/compat';
import {required} from '@angular/forms/signals';

@Component({
  // ...
  imports: [ReactiveFormsModule],
})
export class UserProfile {
  // 1. Create a SignalFormControl, use signal form rules.
  emailControl = new SignalFormControl('', (p) => {
    required(p, {message: 'Email is required'});
  });

  // 2. Use it in an existing FormGroup
  form = new FormGroup({
    email: this.emailControl,
  });
}
```

`SignalFormControl` qiymatlarni **Signal Forms** tizimi va **reaktiv formalar** tizimi oʻrtasida ikki yoʻnalishda sinxronlaydi:

- **Signal -> Reaktiv**: Qiymatni Signal Forms orqali yangilash reaktiv forma kontrolini darhol yangilaydi.

```typescript
// Signal Forms update
this.emailControl.fieldTree().value.set('new@example.com');

// Reactive Forms reflects the change
console.log(this.form.value); // {email: 'new@example.com'}
```

- **Reaktiv -> Signal**: Qiymatni ota `FormGroup` orqali yangilash Signal Forms holatini yangilaydi.

```typescript
// Reactive Forms update
this.form.patchValue({email: 'other@example.com'});

// Signal Forms reflects the change
console.log(this.emailControl.fieldTree().value()); // 'other@example.com'
```

### `SignalFormControl`'ni bogʻlash {#binding-signalformcontrol}

`SignalFormControl`'ni `FormGroup`'da ishlatish uchun uni kontrol sifatida uzating va shablonda `.fieldTree` yordamida bogʻlang:

```typescript
readonly emailControl = new SignalFormControl('', (p) => { required(p); });

readonly form = new FormGroup({
  name: new FormControl('Alice'),
  email: this.emailControl,
});
```

```angular-html {prefer}
<form [formGroup]="form">
  <!-- Standard control -->
  <input formControlName="name" />

  <!-- Signal control -->
  <input [formField]="emailControl.fieldTree" />
</form>
```

```angular-html {avoid}
<!-- Avoid: Using formControlName or [formControl] for SignalFormControl -->
<input formControlName="email" />
<input [formControl]="emailControl" />
```

### Nima uchun `SignalFormControl` signal oʻrniga qiymat qabul qiladi {#why-signalformcontrol-takes-a-value-instead-of-a-signal}

Standart Signal Forms'da formani signal uzatib yaratasiz: `form(mySignal)`.

Biroq, `SignalFormControl` birinchi argument sifatida **xom qiymat** (masalan, satr yoki obyekt) qabul qiladi:

```typescript
// Takes a raw value, not a signal
const userControl = new SignalFormControl({
  email: 'pirojok@example.com',
});
```

`SignalFormControl` yozishlarni ushlab qolish va reaktiv formalar kutadigan **sinxron yangilanishlarni** ishga tushirish uchun signalni ichki ravishda yaratadi.

Ichki signalga `.sourceValue` orqali hali ham murojaat qilishingiz mumkin:

```typescript
const value = userControl.sourceValue();
```

### Kontrolni oʻchirish/yoqish {#disabling-enabling-control}

Yoqilgan/oʻchirilgan holatni oʻzgartirish uchun imperativ API'lar (masalan, `enable()`, `disable()`) `SignalFormControl`'da
ataylab qoʻllab-quvvatlanmaydi. Chunki kontrol holati signal holati va qoidalardan hosil qilinishi kerak.

disable/enable'ni chaqirishga urinish xatoga olib keladi.

```typescript {avoid}
import {signal, effect} from '@angular/core';

export class UserProfile {
  readonly emailControl = new SignalFormControl('');

  readonly isLoading = signal(false);

  constructor() {
    // This will throw an error
    effect(() => {
      if (this.isLoading()) {
        this.emailControl.disable();
      } else {
        this.emailControl.enable();
      }
    });
  }
}
```

Buning oʻrniga disabled qoidasidan foydalaning:

```typescript {prefer}
import {signal} from '@angular/core';
import {SignalFormControl} from '@angular/forms/signals/compat';
import {disabled} from '@angular/forms/signals';

export class UserProfile {
  readonly isLoading = signal(false);

  readonly emailControl = new SignalFormControl('', (p) => {
    // The control becomes disabled whenever isLoading is true
    disabled(p, {when: () => this.isLoading()});
  });

  async saveData() {
    this.isLoading.set(true);
    // ... perform save ...
    this.isLoading.set(false);
  }
}
```

### Dinamik boshqarish {#dynamic-manipulation}

Validatorlarni qoʻshish yoki olib tashlash uchun imperativ API'lar (masalan, `addValidators()`, `removeValidators()`, `setValidators()`)
`SignalFormControl`'da ataylab qoʻllab-quvvatlanmaydi.

Ushbu metodlarni chaqirishga urinish xatoga olib keladi.

```typescript {avoid}
export class UserProfile {
  readonly emailControl = new SignalFormControl('');
  readonly isRequired = signal(false);

  toggleRequired() {
    this.isRequired.update((v) => !v);
    // This will throw an error
    if (this.isRequired()) {
      this.emailControl.addValidators(Validators.required);
    } else {
      this.emailControl.removeValidators(Validators.required);
    }
  }
}
```

Buning oʻrniga validatorlarni shartli qoʻllash uchun `applyWhen` qoidasidan foydalaning:

```typescript {prefer}
import {signal} from '@angular/core';
import {SignalFormControl} from '@angular/forms/signals/compat';
import {applyWhen, required} from '@angular/forms/signals';

export class UserProfile {
  readonly isRequired = signal(false);

  readonly emailControl = new SignalFormControl('', (p) => {
    // The control becomes required whenever isRequired is true
    applyWhen(
      p,
      () => this.isRequired(),
      (p) => {
        required(p);
      },
    );
  });
}
```

### Xatolarni qoʻlda belgilash {#manual-error-selection}

`setErrors()` va `markAsPending()` metodlari qoʻllab-quvvatlanmaydi. Signal Forms'da xatolar validatsiya
qoidalari va asinxron validatsiya holatidan hosil qilinadi. Agar xato haqida xabar berish kerak boʻlsa, bu sxemadagi validatsiya qoidasi orqali
deklarativ tarzda bajarilishi kerak.

## Avtomatik holat klasslari {#automatic-status-classes}

Reaktiv/shablonga asoslangan formalar kontrol holatlariga stil berishni osonlashtirish uchun avtomatik ravishda [class atributlarini](/guide/forms/template-driven-forms#track-control-states) (
masalan, `.ng-valid` yoki `.ng-dirty`) qoʻshadi. Signal Forms buni qilmaydi.

Agar bu xatti-harakatni saqlab qolmoqchi boʻlsangiz, `NG_STATUS_CLASSES` presetini taqdim etishingiz mumkin:

```typescript
import {provideSignalFormsConfig} from '@angular/forms/signals';
import {NG_STATUS_CLASSES} from '@angular/forms/signals/compat';

bootstrapApplication(App, {
  providers: [
    provideSignalFormsConfig({
      classes: NG_STATUS_CLASSES,
    }),
  ],
});
```

Shuningdek, oʻz maxsus logikangizga asoslanib istalgan klasslarni qoʻllash uchun oʻz maxsus konfiguratsiyangizni ham taqdim etishingiz mumkin:

```typescript
import {provideSignalFormsConfig} from '@angular/forms/signals';

bootstrapApplication(App, {
  providers: [
    provideSignalFormsConfig({
      classes: {
        'ng-valid': ({state}) => state().valid(),
        'ng-invalid': ({state}) => state().invalid(),
        'ng-touched': ({state}) => state().touched(),
        'ng-dirty': ({state}) => state().dirty(),
      },
    }),
  ],
});
```

## Maxsus kontrollar {#custom-controls}

Har qanday [maxsus Signal Form kontroli](guide/forms/signals/custom-controls) reaktiv (va shablonga asoslangan) formalar bilan
oʻzgarishsiz ishlatilishi mumkin. Bu mavjud `ControlValueAccessor` implementatsiyalarini mavjud foydalanishlarni buzmasdan
`FormValueControl`/`FormCheckboxControl`'ga migratsiya qilish imkonini beradi.

IMPORTANT: Bir komponentda `ControlValueAccessor` va `FormValueControl`/`FormCheckboxControl`'ning ikkalasini ham
implementatsiya **qilmang**. Ulardan birini implementatsiya qiling.

Quyidagi maxsus kontrol berilgan deylik:

```angular-ts
import {Component, model} from '@angular/core';
import {FormValueControl} from '@angular/forms/signals';

@Component({
  selector: 'app-basic-input',
  template: `
    <div class="basic-input">
      <input
        type="text"
        [value]="value()"
        (input)="value.set($event.target.value)"
        placeholder="Enter text..."
      />
    </div>
  `,
})
export class BasicInput implements FormValueControl<string> {
  /** The current input value */
  value = model('');
}
```

Ushbu maxsus kontrolni reaktiv formalar bilan tabiiy (native) input yoki `ControlValueAccessor`'ga asoslangan maxsus kontrol kabi
ishlatishingiz mumkin. Masalan, reaktiv formaga ega ushbu
oddiy komponentni koʻrib chiqaylik.

```angular-ts
import {Component} from '@angular/core';
import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';
import {BasicInput} from './basic-input';

@Component({
  selector: 'app-example',
  template: `
    <form [formGroup]="reactiveFormGroup">
      <app-basic-input formControlName="reactiveControlName" />
    </form>
    <p>Text: {{ reactiveFormGroup.value.reactiveControlName }}</p>
  `,
  imports: [ReactiveFormsModule, BasicInput],
})
export class ExampleComponent {
  readonly reactiveFormGroup = new FormGroup({
    reactiveControlName: new FormControl(''),
  });
}
```

Maxsus `app-basic-input` kontrolidagi har qanday oʻzgarish reaktiv `FormControl`'da
aks etadi.
