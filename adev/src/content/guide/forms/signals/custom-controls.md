# Maxsus boshqaruv elementlari

NOTE: Bu qoʻllanma siz [Signal Forms asoslari](essentials/signal-forms) bilan tanish ekanligingizni nazarda tutadi.

Brauzerning oʻrnatilgan forma boshqaruv elementlari (input, select, textarea kabi) keng tarqalgan holatlarni qamrab oladi, lekin ilovalarga koʻpincha ixtisoslashgan input'lar kerak boʻladi. Kalendar UI'ga ega sana tanlagich, formatlash paneliga ega boy matn muharriri yoki avtomatik toʻldirishga ega teg tanlagich — bularning barchasi maxsus implementatsiyani talab qiladi.

Signal Forms maʼlum interfeyslarni implementatsiya qiluvchi istalgan komponent bilan ishlaydi. **Boshqaruv elementi interfeysi** (control interface) komponentingizning forma tizimi bilan muloqot qilishiga imkon beruvchi xususiyatlar va signallarni belgilaydi. Komponentingiz shu interfeyslardan birini implementatsiya qilsa, `[formField]` direktivi boshqaruv elementingizni forma holati, validatsiya va maʼlumotlarni bogʻlashga avtomatik ulaydi.

HELPFUL: Maxsus Signal Form boshqaruv elementlari hech qanday qoʻshimcha moslik kodisiz Signal, Reactive va Template-Driven formalar bilan [ishlatilishi mumkin](guide/forms/signals/migration#custom-controls).

## Asosiy maxsus boshqaruv elementini yaratish {#creating-a-basic-custom-control}

Minimal implementatsiyadan boshlab, kerak boʻlganda imkoniyatlar qoʻshib boramiz.

### Minimal input boshqaruv elementi {#minimal-input-control}

Asosiy maxsus input faqat `FormValueControl` interfeysini implementatsiya qilishi va talab qilinadigan `value` model signalini belgilashi kerak.

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

### Minimal belgilash katakchasi (checkbox) boshqaruv elementi {#minimal-checkbox-control}

Checkbox uslubidagi boshqaruv elementi uchun ikki narsa kerak:

1. `FormField` direktivi uni forma boshqaruv elementi sifatida tanishi uchun `FormCheckboxControl` interfeysini implementatsiya qilish
2. `checked` model signalini taqdim etish

```angular-ts
import {Component, model, ChangeDetectionStrategy} from '@angular/core';
import {FormCheckboxControl} from '@angular/forms/signals';

@Component({
  selector: 'app-basic-toggle',
  template: `
    <button type="button" [class.active]="checked()" (click)="toggle()">
      <span class="toggle-slider"></span>
    </button>
  `,
})
export class BasicToggle implements FormCheckboxControl {
  /** Whether the toggle is checked */
  checked = model<boolean>(false);

  toggle() {
    this.checked.update((val) => !val);
  }
}
```

### Maxsus boshqaruv elementingizdan foydalanish {#using-your-custom-control}

Boshqaruv elementini yaratganingizdan soʻng, unga `FormField` direktivini qoʻshib, undan oʻrnatilgan input ishlatiladigan istalgan joyda foydalanishingiz mumkin:

```angular-ts
import {Component, signal, ChangeDetectionStrategy} from '@angular/core';
import {form, FormField, required} from '@angular/forms/signals';
import {BasicInput} from './basic-input';
import {BasicToggle} from './basic-toggle';

@Component({
  imports: [FormField, BasicInput, BasicToggle],
  template: `
    <form novalidate>
      <label>
        Email
        <app-basic-input [formField]="registrationForm.email" />
      </label>

      <label>
        Accept terms
        <app-basic-toggle [formField]="registrationForm.acceptTerms" />
      </label>

      <button type="submit" [disabled]="registrationForm().invalid()">Register</button>
    </form>
  `,
})
export class Registration {
  registrationModel = signal({
    email: '',
    acceptTerms: false,
  });

  registrationForm = form(this.registrationModel, (schemaPath) => {
    required(schemaPath.email, {message: 'Email is required'});
    required(schemaPath.acceptTerms, {message: 'You must accept the terms'});
  });
}
```

NOTE: Sxema callback parametri (bu misollarda `schemaPath`) formangizdagi barcha maydonlarga yoʻllarni taqdim etuvchi `SchemaPathTree` obyektidir. Bu parametrni istalgancha nomlashingiz mumkin.

`[formField]` direktivi maxsus boshqaruv elementlari va oʻrnatilgan input'lar uchun bir xil ishlaydi. Signal Forms ularga bir xil munosabatda boʻladi — validatsiya bajariladi, holat yangilanadi va maʼlumotlarni bogʻlash avtomatik ishlaydi.

## Boshqaruv elementi interfeyslarini tushunish {#understanding-control-interfaces}

Maxsus boshqaruv elementlarini amalda koʻrganingizdan soʻng, ularning Signal Forms bilan qanday integratsiyalashuvini koʻrib chiqamiz.

### Boshqaruv elementi interfeyslari {#control-interfaces}

Siz yaratgan `BasicInput` va `BasicToggle` komponentlari Signal Forms'ga ular bilan qanday ishlashni bildiruvchi maʼlum boshqaruv elementi interfeyslarini implementatsiya qiladi.

#### FormValueControl

`FormValueControl` — koʻpchilik input turlari uchun interfeys: matnli input'lar, sonli input'lar, sana tanlagichlar, tanlov roʻyxatlari (select) va bitta qiymatni tahrirlovchi istalgan boshqaruv elementi. Komponentingiz bu interfeysni implementatsiya qilganda:

- **Talab qilinadigan xususiyat**: Komponentingiz `value` model signalini taqdim etishi shart
- **FormField direktivi nima qiladi**: Forma maydonining qiymatini boshqaruv elementingizning `value` signaliga bogʻlaydi

IMPORTANT: `FormValueControl`'ni implementatsiya qiluvchi boshqaruv elementlarida `checked` xususiyati boʻlmasligi SHART

#### FormCheckboxControl

`FormCheckboxControl` — checkbox'ga oʻxshash boshqaruv elementlari uchun interfeys: toggle'lar, switch'lar va boolean yoqilgan/oʻchirilgan holatini ifodalovchi istalgan boshqaruv elementi. Komponentingiz bu interfeysni implementatsiya qilganda:

- **Talab qilinadigan xususiyat**: Komponentingiz `checked` model signalini taqdim etishi shart
- **FormField direktivi nima qiladi**: Forma maydonining qiymatini boshqaruv elementingizning `checked` signaliga bogʻlaydi

IMPORTANT: `FormCheckboxControl`'ni implementatsiya qiluvchi boshqaruv elementlarida `value` xususiyati boʻlmasligi SHART

### Ixtiyoriy holat xususiyatlari {#optional-state-properties}

`FormValueControl` ham, `FormCheckboxControl` ham `FormUiControl`'ni kengaytiradi — bu forma holati bilan integratsiya qilish uchun ixtiyoriy xususiyatlarni taqdim etuvchi asosiy interfeys.

Barcha xususiyatlar ixtiyoriy. Faqat boshqaruv elementingizga kerak boʻlganlarini implementatsiya qiling.

#### Oʻzaro aloqa holati {#interaction-state}

Foydalanuvchilar boshqaruv elementingiz bilan qachon oʻzaro aloqa qilganini kuzating:

| Xususiyat | Vazifasi                                                  |
| --------- | --------------------------------------------------------- |
| `touched` | Foydalanuvchi maydon bilan oʻzaro aloqa qilgan-qilmagani  |
| `dirty`   | Qiymat dastlabki holatidan farq qiladimi-yoʻqmi           |

#### Validatsiya holati {#validation-state}

Foydalanuvchilarga validatsiya natijalarini koʻrsating:

| Xususiyat | Vazifasi                                          |
| --------- | ------------------------------------------------- |
| `errors`  | Joriy validatsiya xatolari massivi                |
| `invalid` | Maydonda validatsiya xatolari bormi-yoʻqmi        |
| `pending` | Asinxron validatsiya davom etayotganmi-yoʻqmi     |

#### Mavjudlik holati {#availability-state}

Foydalanuvchilar maydoningiz bilan oʻzaro aloqa qila olishini boshqaring:

| Xususiyat         | Vazifasi                                                              |
| ----------------- | --------------------------------------------------------------------- |
| `disabled`        | Maydon oʻchirilganmi-yoʻqmi                                           |
| `disabledReasons` | Maydonning oʻchirilganlik sabablari                                   |
| `readonly`        | Maydon faqat oʻqish uchunmi-yoʻqmi (koʻrinadi, lekin tahrirlanmaydi)  |
| `hidden`          | Maydon koʻrinishdan yashirilganmi-yoʻqmi                              |

NOTE: `disabledReasons` — `DisabledReason` obyektlari massivi. Har bir obyektda `fieldTree` xususiyati (maydonlar daraxtiga havola) va ixtiyoriy `message` xususiyati bor. Xabarga `reason.message` orqali murojaat qiling.

#### Validatsiya cheklovlari {#validation-constraints}

Formadan validatsiya cheklovi qiymatlarini qabul qiling:

| Xususiyat   | Vazifasi                                                   |
| ----------- | ---------------------------------------------------------- |
| `required`  | Maydon majburiymi-yoʻqmi                                   |
| `min`       | Minimal sonli qiymat (cheklov boʻlmasa `undefined`)        |
| `max`       | Maksimal sonli qiymat (cheklov boʻlmasa `undefined`)       |
| `minLength` | Minimal satr uzunligi (cheklov boʻlmasa undefined)         |
| `maxLength` | Maksimal satr uzunligi (cheklov boʻlmasa undefined)        |
| `pattern`   | Moslik tekshiriladigan regulyar ifoda namunalari massivi   |

#### Maydon metamaʼlumotlari {#field-metadata}

| Xususiyat | Vazifasi                                                                  |
| --------- | ------------------------------------------------------------------------- |
| `name`    | Maydonning name atributi (formalar va ilovalar boʻylab yagona boʻladi)    |

Quyidagi "[Holat signallarini qoʻshish](#adding-state-signals)" boʻlimi bu xususiyatlarni boshqaruv elementlaringizda qanday implementatsiya qilishni koʻrsatadi.

### FormField direktivi qanday ishlaydi {#how-the-formfield-directive-works}

`[formField]` direktivi boshqaruv elementingiz qaysi interfeysni implementatsiya qilganini aniqlaydi va tegishli signallarni avtomatik bogʻlaydi:

```angular-ts
import {Component, signal, ChangeDetectionStrategy} from '@angular/core';
import {form, FormField, required} from '@angular/forms/signals';
import {CustomInput} from './custom-input';
import {CustomToggle} from './custom-toggle';

@Component({
  selector: 'app-my-form',
  imports: [FormField, CustomInput, CustomToggle],
  template: `
    <form novalidate>
      <app-custom-input [formField]="userForm.username" />
      <app-custom-toggle [formField]="userForm.subscribe" />
    </form>
  `,
})
export class MyForm {
  formModel = signal({
    username: '',
    subscribe: false,
  });

  userForm = form(this.formModel, (schemaPath) => {
    required(schemaPath.username, {message: 'Username is required'});
  });
}
```

TIP: Forma modellarini yaratish va boshqarish haqida toʻliq maʼlumot uchun [Forma modellari boʻyicha qoʻllanma](guide/forms/signals/models) bilan tanishing.

`[formField]="userForm.username"` deb bogʻlaganingizda, FormField direktivi:

1. Boshqaruv elementingiz `FormValueControl`'ni implementatsiya qilganini aniqlaydi
2. Ichki tarzda `userForm.username().value()`'ga murojaat qiladi va uni boshqaruv elementingizning `value` model signaliga bogʻlaydi
3. Forma holati signallarini (`disabled()`, `errors()` va boshqalar) boshqaruv elementingizning ixtiyoriy input signallariga bogʻlaydi
4. Yangilanishlar signal reaktivligi orqali avtomatik sodir boʻladi

## Holat signallarini qoʻshish {#adding-state-signals}

Yuqorida koʻrsatilgan minimal boshqaruv elementlari ishlaydi, lekin forma holatiga javob bermaydi. Boshqaruv elementlaringiz oʻchirilgan holatga reaksiya qilishi, validatsiya xatolarini koʻrsatishi va foydalanuvchi oʻzaro aloqasini kuzatishi uchun ixtiyoriy input signallarni qoʻshishingiz mumkin.

Keng tarqalgan holat xususiyatlarini implementatsiya qiluvchi keng qamrovli misol:

```angular-ts
import {Component, model, input, output, ChangeDetectionStrategy} from '@angular/core';
import {
  FormValueControl,
  WithOptionalFieldTree,
  ValidationError,
  DisabledReason,
} from '@angular/forms/signals';

@Component({
  selector: 'app-stateful-input',
  template: `
    @if (!hidden()) {
      <div class="input-container">
        <input
          type="text"
          [value]="value()"
          (input)="value.set($event.target.value)"
          [disabled]="disabled()"
          [readonly]="readonly()"
          [class.invalid]="invalid()"
          [attr.aria-invalid]="invalid()"
          (blur)="touch.emit()"
        />

        @if (invalid()) {
          <div class="error-messages" role="alert">
            @for (error of errors(); track error) {
              <span class="error">{{ error.message }}</span>
            }
          </div>
        }

        @if (disabled() && disabledReasons().length > 0) {
          <div class="disabled-reasons">
            @for (reason of disabledReasons(); track reason) {
              <span>{{ reason.message }}</span>
            }
          </div>
        }
      </div>
    }
  `,
})
export class StatefulInput implements FormValueControl<string> {
  // Required
  value = model<string>('');

  // Writable interaction state - control updates these
  touched = input<boolean>(false);
  touch = output<void>();

  // Read-only state - form system manages these
  disabled = input<boolean>(false);
  disabledReasons = input<readonly WithOptionalFieldTree<DisabledReason>[]>([]);
  readonly = input<boolean>(false);
  hidden = input<boolean>(false);
  invalid = input<boolean>(false);
  errors = input<readonly WithOptionalFieldTree<ValidationError>[]>([]);
}
```

Natijada boshqaruv elementidan validatsiya va holatni boshqarish bilan birga foydalanishingiz mumkin:

```angular-ts
import {Component, signal, ChangeDetectionStrategy} from '@angular/core';
import {form, FormField, required, email} from '@angular/forms/signals';
import {StatefulInput} from './stateful-input';

@Component({
  imports: [FormField, StatefulInput],
  template: `
    <form novalidate>
      <label>
        Email
        <app-stateful-input [formField]="loginForm.email" />
      </label>
    </form>
  `,
})
export class Login {
  loginModel = signal({email: ''});

  loginForm = form(this.loginModel, (schemaPath) => {
    required(schemaPath.email, {message: 'Email is required'});
    email(schemaPath.email, {message: 'Enter a valid email address'});
  });
}
```

Foydalanuvchi notoʻgʻri email kiritganda, FormField direktivi `invalid()` va `errors()`'ni avtomatik yangilaydi. Boshqaruv elementingiz validatsiya natijalarini koʻrsatishi mumkin.

### `debounce('blur')` bilan ishlash {#working-with-debounceblur}

[`debounce('blur')`](api/forms/signals/debounce) qoidasi UI'dan forma modeliga yangilanishlarni har bir tugma bosilishida qoʻllash oʻrniga, maydon fokusni yoʻqotguncha (blur) kechiktiradi. Oʻrnatilgan boshqaruv elementlari blur haqida formaga avtomatik xabar beradi. Maxsus boshqaruv elementi esa bunda faqat tabiiy [`blur` hodisasiga](https://developer.mozilla.org/en-US/docs/Web/API/Element/blur_event) javoban oʻz `touch` output'ini chiqarsa ishtirok etadi:

```angular-ts
import {Component, model, output} from '@angular/core';
import {FormValueControl} from '@angular/forms/signals';

@Component({
  selector: 'app-custom-input',
  template: `
    <input
      type="text"
      [value]="value()"
      (input)="value.set($event.target.value)"
      (blur)="touch.emit()"
    />
  `,
})
export class CustomInput implements FormValueControl<string> {
  value = model('');
  touch = output<void>();
}
```

`touch` output'i mavjud boʻlganda, `debounce('blur')` boshqaruv elementingiz uchun oʻrnatilgan input'lar bilan bir xil ishlaydi:

```angular-ts
import {Component, signal} from '@angular/core';
import {debounce, form, FormField} from '@angular/forms/signals';
import {CustomInput} from './custom-input';

@Component({
  selector: 'app-root',
  imports: [CustomInput, FormField],
  template: `<app-custom-input [formField]="userForm.name" />`,
})
export class App {
  userModel = signal({name: ''});

  userForm = form(this.userModel, (schemaPath) => {
    debounce(schemaPath.name, 'blur');
  });
}
```

IMPORTANT: `touch`'ni `focus`'da emas, `blur`'da (fokus boshqaruv elementidan chiqqanda) chiqaring. `touch` output'isiz maydon hech qachon blur qilingan deb qayd etilmaydi, shuning uchun `debounce('blur')` boshqaruv elementingizga taʼsir qilmaydi.

## Qiymatni transformatsiya qilish {#value-transformation}

Boshqaruv elementlari baʼzan qiymatlarni forma modeli saqlaganidan farqli koʻrsatadi — sana tanlagich "2024-01-15"ni saqlab, "January 15, 2024" deb koʻrsatishi, yoki valyuta input'i 1234.56 ni saqlab, "$1,234.56" deb koʻrsatishi mumkin.

UI'da koʻrsatiladigan xom qiymatni model qiymati bilan sinxron saqlash uchun `transformedValue()`'dan (`@angular/forms/signals`'dan) foydalaning. U boshqaruv elementining `value` model signalini hamda `parse` va `format` funksiyalarini qabul qiladi va xom qiymatni saqlovchi yoziladigan signalni qaytaradi:

- `format` model qiymatini shablon render qiladigan xom qiymatga aylantiradi.
- `parse` foydalanuvchi kiritgan matnni model qiymatiga qaytaradi va uning oʻrniga tahlil (parse) xatolari haqida xabar berishi ham mumkin.

```angular-ts
import {Component, model} from '@angular/core';
import {FormValueControl, transformedValue} from '@angular/forms/signals';

@Component({
  selector: 'number-input',
  template: `
    <input type="text" [value]="rawValue()" (input)="rawValue.set($event.target.value)" />
  `,
})
export class NumberInput implements FormValueControl<number | null> {
  readonly value = model.required<number | null>();

  protected readonly rawValue = transformedValue(this.value, {
    parse: (val: string): {value: number | null} => ({value: val ? Number(val) : null}),
    format: (val: number | null): string => val?.toString() ?? '',
  });
}
```

Qaytarilgan signalga yozish (`rawValue.set(...)`) `parse`'ni ishga tushiradi va natijani `value`'ga yozadi. Model boshqa joydan oʻzgarganda — `reset()`, sxema qoidasi yoki ilovaning boshqa qismi orqali — `format` qayta ishga tushadi va xom qiymat unga mos ravishda yangilanadi.

### Tahlil xatolari haqida xabar berish {#reporting-parse-errors}

Baʼzan xom qiymatning yaroqli model ifodasi boʻlmaydi — chala kiritilgan sana yoki sonli maydondagi harflar. Yuqoridagi `NumberInput`'da shu muammo bor: `Number('abc')` natijasi `NaN` boʻlib, `parse` uni bemalol modelga yozadi.

Uning oʻrniga `{error}` qaytaring:

```ts
export class NumberInput implements FormValueControl<number | null> {
  readonly value = model.required<number | null>();

  protected readonly rawValue = transformedValue(this.value, {
    parse: (val) => {
      const parsed = val ? Number(val) : null;

      return Number.isNaN(parsed)
        ? {error: {kind: 'parse', message: `${val} is not a number`}}
        : {value: parsed};
    },
    format: (val) => val?.toString() ?? '',
  });
}
```

Modelni yangilash _va_ muammoni belgilash kerak boʻlganda `value`'ni ham, `error`'ni ham qaytaring.

Boshqaruv elementi `[formField]` bilan bogʻlanganda tahlil xatolari maydonga avtomatik yetkaziladi, shuning uchun ular validatsiya xatolari bilan birga maydonning `errors()` signalida koʻrinadi:

```angular-ts
@Component({
  imports: [NumberInput, FormField],
  template: `
    <number-input [formField]="orderForm.amount" />

    @for (error of orderForm.amount().errors(); track $index) {
      <!-- {kind: 'parse', message: '...'} is reported here too -->
      <p class="error">{{ error.message }}</p>
    }
  `,
})
export class Order {
  orderModel = signal<{amount: number | null}>({amount: null});
  orderForm = form(this.orderModel);
}
```

Tahlil xatolari boʻlgan maydon invalid hisoblanadi, bu esa muvaffaqiyatsiz validatsiya qoidasi kabi yuborishni bloklaydi.

HELPFUL: Signal Forms tabiiy input'lar uchun ham xuddi shu mexanizmdan foydalanadi. Brauzer qiymatni tahlil qila olmasa (masalan, `<input type="date">`'da qisman kiritilgan sana), bu maydonda `parse` xatosi sifatida namoyon boʻladi. Tafsilotlar uchun [Tabiiy HTML validatsiyasi](guide/forms/signals/validation#native-html-validation) boʻlimiga qarang.

### Qayta tiklash {#resetting}

Maydonda `reset()`'ni chaqirish kutilayotgan tahlil xatolarini tozalaydi va xom qiymatni modeldan qayta formatlaydi, shuning uchun tahlil qilib boʻlmaydigan holatda qolgan boshqaruv elementi toza koʻrsatiladigan qiymatga qaytadi:

```ts
orderForm.amount().reset();
```

## Validatsiya bilan integratsiya {#validation-integration}

Boshqaruv elementlari validatsiya holatini koʻrsatadi, lekin validatsiyani bajarmaydi. Validatsiya forma sxemasida sodir boʻladi — boshqaruv elementingiz FormField direktividan `invalid()` va `errors()` signallarini qabul qiladi va ularni koʻrsatadi (yuqoridagi StatefulInput misolida koʻrsatilganidek).

FormField direktivi shuningdek `required`, `min`, `max`, `minLength`, `maxLength` va `pattern` kabi validatsiya cheklovi qiymatlarini ham uzatadi. Boshqaruv elementingiz UI'ni yaxshilash uchun ulardan foydalanishi mumkin:

```ts
export class NumberInput implements FormValueControl<number> {
  value = model<number>(0);

  // Constraint values from schema validation rules
  required = input<boolean>(false);
  min = input<number | undefined>(undefined);
  max = input<number | undefined>(undefined);
}
```

Sxemaga `min()` va `max()` validatsiya qoidalarini qoʻshganingizda, FormField direktivi bu qiymatlarni boshqaruv elementingizga uzatadi. Ulardan HTML5 atributlarini qoʻllash yoki shablonda cheklov haqida koʻrsatmalar chiqarish uchun foydalaning.

IMPORTANT: Validatsiya mantigʻini boshqaruv elementingizda implementatsiya qilmang. Validatsiya qoidalarini forma sxemasida belgilang va boshqaruv elementingiz natijalarni koʻrsatsin:

```ts {avoid}
// Avoid: Validation in control
export class BadControl implements FormValueControl<string> {
  value = model<string>('');
  isValid() {
    return this.value().length >= 8;
  } // Don't do this!
}
```

```ts {prefer}
// Good: Validation in schema, control displays results
accountForm = form(this.accountModel, (schemaPath) => {
  minLength(schemaPath.password, 8, {message: 'Password must be at least 8 characters'});
});
```

## Boshqaruv elementlarini qayta ishlatiladigan qilish {#making-controls-reusable}

Maxsus boshqaruv elementi koʻpincha validatsiya haqida yashirin kutilmalarga ega boʻladi. Email input'i uni ishlatadigan har bir formada `required` va `email` qoidalarini talab qiladi. Har bir isteʼmolchi bu qoidalarni qayta eʼlon qilishiga tayanish oʻrniga, boshqaruv elementi bilan birga hamroh sxemani paketlang va ikkalasini bir xil modulda eksport qiling:

```ts {header: 'email-input.ts'}
import {schema, required, email} from '@angular/forms/signals';

export const emailFieldSchema = schema<string>((path) => {
  required(path, {message: 'Email is required'});
  email(path, {message: 'Enter a valid email address'});
});
```

Isteʼmolchi hamroh sxemani import qiladi va `apply()` yordamida uni oʻz formasiga kompozitsiya qiladi:

```ts {header: 'registration.ts'}
import {form, apply} from '@angular/forms/signals';
import {emailFieldSchema} from './email-input';

registrationForm = form(this.registrationModel, (path) => {
  apply(path.email, emailFieldSchema);
});
```

`apply()` hamroh sxemaning qoidalarini belgilangan yoʻlda asosiy formaga birlashtiradi. Isteʼmolchi oʻsha maydonga yana qoidalar qoʻshishi mumkin, chunki `apply()` boshqa qoidalarni almashtirmaydi, balki ular bilan kompozitsiya qilinadi. `schema()`, `apply()` va `applyWhen()` bilan shartli kompozitsiya haqida toʻliq maʼlumot uchun [Sxemalar boʻyicha qoʻllanma](guide/forms/signals/schemas) bilan tanishing.

### Dizayn boʻyicha mulohazalar {#design-considerations}

Isteʼmolchining modeli har bir maydonni aniqlangan qiymat bilan ishga tushirishi shart. Signal Forms'da `undefined` boʻsh qiymatni emas, maydonning yoʻqligini bildiradi. Qayta ishlatiladigan email boshqaruv elementi uchun bu isteʼmolchi xususiyatni undefined holda qoldirmasdan, dastlabki qiymat sifatida `''` ishlatishi kerakligini anglatadi. Dastlabki qiymatlarni tanlash boʻyicha tafsilotlar uchun [Forma modellari boʻyicha qoʻllanma](guide/forms/signals/models) bilan tanishing.

Bundan tashqari, boshqaruv elementlari holatni boshqarish uchun oʻz effect'larini roʻyxatdan oʻtkazmasligi kerak. Forma tizimi maydon holatini ichki effect'lar orqali boshqaradi. Bu boshqaruv elementingiz holat yangilanishlarini input signallar orqali olishini anglatadi. Boshqaruv elementi qiymatlarni transformatsiya qilishi kerak boʻlsa, `effect()` oʻrniga "[Qiymatni transformatsiya qilish](#value-transformation)" boʻlimida koʻrsatilganidek `transformedValue()`'dan foydalaning.

## Keyingi qadamlar {#next-steps}

Bu qoʻllanma Signal Forms bilan integratsiyalashuvchi maxsus boshqaruv elementlarini yaratishni yoritdi. Tegishli qoʻllanmalar Signal Forms'ning boshqa jihatlarini koʻrib chiqadi:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/models" title="Forma modellari" />
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <!-- <docs-pill href="guide/forms/signals/arrays" title="Massivlar bilan ishlash" /> -->
</docs-pill-row>
