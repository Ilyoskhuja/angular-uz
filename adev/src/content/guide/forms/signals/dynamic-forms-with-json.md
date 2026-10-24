# JSON bilan dinamik formalar

Baʼzi formalar oʻz tuzilmasini kompilyatsiya vaqtida belgilay olmaydi. Server tomonidan boshqariladigan formalar, admin panellar, koʻp ijarachili (multi-tenant) ilovalar va CMS orqali boshqariladigan kontent — bularning barchasi maydonlarni ish vaqtida (runtime) yetkazib beriladigan konfiguratsiyadan, odatda backend, admin vositasi yoki har bir ijarachi uchun alohida sozlamalardan keladigan JSON'dan render qilishi kerak.

Ushbu qoʻllanma modeli, sxemasi, validatsiyasi va render qilinishi yagona runtime konfiguratsiyasidan hosil qilinadigan formalarni qanday yaratishni koʻrsatadi.

## JSON asosidagi formalardan qachon foydalanish kerak {#when-to-use-json-driven-forms}

Bu namuna quyidagi hollarda yaxshi tanlov boʻladi:

- Backend foydalanuvchi roli, feature flag'lar yoki biznes qoidalariga qarab qaysi maydonlar koʻrinishini belgilaydi
- Dasturchi boʻlmagan foydalanuvchilar forma tuzilmasini admin panel yoki CMS orqali sozlaydi
- Koʻp ijarachili ilovada har bir ijarachining konfiguratsiya sifatida saqlanadigan oʻz forma tuzilmasi bor
- Formalar frontend'ni qayta deploy qilmasdan rivojlanishi kerak

Tuzilma build vaqtida maʼlum boʻlsa, statik formadan (maydonlari bevosita komponentingizda belgilangan) foydalaning. Statik formalar har bir maydon uchun toʻliq TypeScript tekshiruvini, shuningdek sodda testlash va vositalar yordamini oladi.

## Tiplangan maydon konfiguratsiyasini belgilash {#defining-a-typed-field-config}

Maydonlarni runtime konfiguratsiyasidan render qilmoqchi boʻlsangiz, har bir maydonning shaklini ifodalovchi TypeScript tipidan boshlang. `kind` boʻyicha diskriminatsiyalangan birlashma (discriminated union) har bir variantga oʻz validatsiya parametrlarini eʼlon qilish imkonini beradi:

```ts
type FieldConfig =
  | {kind: 'text'; name: string; label: string; required?: boolean}
  | {kind: 'number'; name: string; label: string; required?: boolean; min?: number; max?: number};
```

Har bir variantda name, label va ixtiyoriy `required` flag'i bor. Sonli maydonlar qoʻshimcha ravishda `min` va `max` chegaralarini qabul qiladi. Yangi variantlarni yangi `kind` shoxlarini qoʻshish orqali qoʻshing.

Aniq konfiguratsiya quyidagicha koʻrinishi mumkin:

```ts
const profileConfig: FieldConfig[] = [
  {kind: 'text', name: 'fullName', label: 'Full Name', required: true},
  {kind: 'number', name: 'age', label: 'Age', required: true, min: 18, max: 120},
];
```

Amalda bu `FieldConfig[]` odatda backend'ingizdan, admin paneldan yoki CMS'dan keladi. Qisqalik uchun quyidagi misollarda komponent ichidagi literal ishlatiladi.

## Konfiguratsiyadan model yaratish {#building-the-model-from-config}

Forma modelida har bir maydon uchun maydon turiga (kind) mos sukut boʻyicha qiymatga ega bitta yozuv boʻlishi kerak. Buni kichik yordamchi funksiya bajaradi:

```ts
function buildModel(configs: FieldConfig[]): Record<string, string | number | null> {
  const initial: Record<string, string | number | null> = {};
  for (const config of configs) {
    initial[config.name] = config.kind === 'number' ? null : '';
  }
  return initial;
}
```

Kalitlar oldindan maʼlum boʻlmagani uchun model `Record<string, string | number | null>` tipidan foydalanadi.

Bundan tashqari, sonli maydonlar `0` emas, `null` bilan ishga tushiriladi, shunda boʻsh maydon boʻsh sifatida oʻqiladi. `0` boʻlsa, [`required()`](api/forms/signals/required) maydonni allaqachon toʻldirilgan deb hisoblar edi, noldan katta har qanday [`min()`](api/forms/signals/min) cheklovi esa foydalanuvchi hali hech narsa kiritmasidan oldin maydonni invalid deb belgilar edi.

## Konfiguratsiyadan sxema yaratish {#building-the-schema-from-config}

Sxema ham konfiguratsiyadan hosil qilinadi. Har bir yozuv boʻylab aylanib, uning turiga mos validatorlarni qoʻllashingiz mumkin:

```ts
import {required, min, max, SchemaFn, SchemaPath} from '@angular/forms/signals';

function buildSchema(configs: FieldConfig[]): SchemaFn<Record<string, string | number | null>> {
  return (path) => {
    for (const config of configs) {
      const fieldPath = path[config.name];

      if (config.required) {
        required(fieldPath);
      }

      if (config.kind === 'number') {
        const numberPath = fieldPath as unknown as SchemaPath<number | null>;
        if (config.min !== undefined) min(numberPath, config.min);
        if (config.max !== undefined) max(numberPath, config.max);
      }
    }
  };
}
```

Diskriminatsiyalangan birlashma har bir shox ichida `config`'ni toraytiradi, shuning uchun `config.kind === 'number'` boʻlganda `config.min` va `config.max` toʻgʻri tiplanadi.

## Shartli qoidalarni konfiguratsiyada ifodalash {#expressing-conditional-rules-in-config}

Baʼzi validatsiya qoidalari faqat maʼlum shartlarda maʼnoga ega. Masalan, AQSh shtat kodlarini faqat mamlakat AQSh boʻlganda tekshirish kerak. Bu bogʻliqliklarni konfiguratsiyada boshqa maydonni va u teng boʻlishi kerak boʻlgan qiymatni koʻrsatuvchi `when` diskriminatorini qoʻshish orqali ifodalang:

```ts
type WhenCondition = {field: string; equals: string | number};

type FieldConfig =
  | {kind: 'text'; name: string; label: string; required?: boolean; when?: WhenCondition}
  | {
      kind: 'number';
      name: string;
      label: string;
      required?: boolean;
      min?: number;
      max?: number;
      when?: WhenCondition;
    };
```

`when`'ni [`applyWhen()`](api/forms/signals/applyWhen) chaqiruviga aylantirish uchun `buildSchema()`'ni yangilang. Qoidalarni qoʻllashning umumiy mantigʻi kichik closure'ga koʻchiriladi, shunda shartli va shartsiz shoxlarning ikkalasi ham bir xil funksiyani chaqiradi:

```ts
import {applyWhen, required, min, max, SchemaFn, SchemaPath} from '@angular/forms/signals';

function buildSchema(configs: FieldConfig[]): SchemaFn<Record<string, string | number | null>> {
  return (rootPath) => {
    for (const config of configs) {
      const applyRules = (path: typeof rootPath) => {
        const fieldPath = path[config.name];
        if (config.required) required(fieldPath);
        if (config.kind === 'number') {
          const numberPath = fieldPath as unknown as SchemaPath<number | null>;
          if (config.min !== undefined) min(numberPath, config.min);
          if (config.max !== undefined) max(numberPath, config.max);
        }
      };

      if (config.when) {
        const {field, equals} = config.when;
        applyWhen(rootPath, ({valueOf}) => valueOf(rootPath[field]) === equals, applyRules);
      } else {
        applyRules(rootPath);
      }
    }
  };
}
```

`applyWhen()` sharti true boʻlganda ichidagi qoidalar faollashadi. Shart false boʻlganda qoidalar oʻchiriladi va maydonning validatsiya holati tozalanadi. Shart funksiyasi `valueOf(rootPath[field])` orqali oʻqigani uchun forma havola qilingan maydon har safar oʻzgarganda shartni qayta hisoblaydi.

`when` ishlatadigan konfiguratsiya quyidagicha koʻrinadi:

```ts
const addressConfig: FieldConfig[] = [
  {kind: 'text', name: 'country', label: 'Country', required: true},
  {
    kind: 'text',
    name: 'stateCode',
    label: 'State',
    required: true,
    when: {field: 'country', equals: 'US'},
  },
];
```

`stateCode` maydoni faqat `country` qiymati `'US'` boʻlganda qiymat talab qiladi. Boshqa istalgan mamlakatni kiritgan foydalanuvchilar `stateCode`'ni boʻsh qoldirishi mumkin va bu yuborishga toʻsqinlik qilmaydi.

Murakkabroq shartlar uchun (bir nechta maydon, diapazonlar yoki tenglik boʻlmagan tekshiruvlar) `WhenCondition`'ni qoʻshimcha diskriminatorlar bilan (masalan, `in: string[]` yoki `notEquals: string | number`) kengaytiring va har bir variantni `buildSchema()` ichida aylantiring. Tamoyil bir xil: konfiguratsiya maʼlumotni tashiydi, `buildSchema()` esa uni `applyWhen()` chaqiruvlariga aylantiradi.

Validatsiya oʻrniga koʻrinishni boshqarish uchun maydon yoʻlida [`hidden()`](api/forms/signals/hidden) ishlatib, shu namunaga amal qiling. Tafsilotlar uchun [Maydonlarda `hidden()` holatini sozlash](guide/forms/signals/form-logic#configuring-hidden-state-on-fields) boʻlimiga qarang.

## Takrorlanuvchi maydonlarni konfiguratsiyada ifodalash {#expressing-repeating-fields-in-config}

Baʼzi konfiguratsiyalarga ish vaqtida koʻpayib-kamayadigan maydonlar kerak boʻladi, masalan, telefon raqamlari, teglar yoki hisob-faktura qatorlari roʻyxati. Konfiguratsiyaga `array` turini qoʻshing va uni [`applyEach()`](api/forms/signals/applyEach)'ga aylantiring, shunda elementlar qoʻshilib-olib tashlanganda har bir element uchun qoidalar bir xilda qoʻllanadi.

`FieldConfig`'ni `array` varianti bilan kengaytiring. Bu misolda satrlar massivlari ishlatiladi; element shaklini record bilan almashtirsangiz, xuddi shu yondashuv obyektlar massivlariga ham kengayadi:

```ts
type FieldConfig =
  | {kind: 'text'; name: string; label: string; required?: boolean; when?: WhenCondition}
  | {
      kind: 'number';
      name: string;
      label: string;
      required?: boolean;
      min?: number;
      max?: number;
      when?: WhenCondition;
    }
  | {kind: 'array'; name: string; label: string; itemRequired?: boolean; when?: WhenCondition};
```

Massiv maydonlarini boʻsh massiv bilan ishga tushirish uchun `buildModel()`'ni yangilang. Model `string[]`'ni ham qamrab olish uchun kengayadi:

```ts
function buildModel(configs: FieldConfig[]): Record<string, string | number | null | string[]> {
  const initial: Record<string, string | number | null | string[]> = {};
  for (const config of configs) {
    if (config.kind === 'number') initial[config.name] = null;
    else if (config.kind === 'array') initial[config.name] = [];
    else initial[config.name] = '';
  }
  return initial;
}
```

Har bir element uchun qoidalarni `applyEach()` bilan qoʻllash uchun `buildSchema()`'ni yangilang. `Record<string, string | number | null | string[]>` modelidan keladigan yoʻl `applyEach()` (hamda `min()` / `max()`) toʻgʻridan-toʻgʻri tip tekshiruvidan oʻtishi uchun juda keng, shuning uchun har bir `kind` shoxi ichida `fieldPath`'ni tegishli shaklga cast qiling:

```ts
import {
  applyEach,
  applyWhen,
  required,
  min,
  max,
  SchemaFn,
  SchemaPath,
} from '@angular/forms/signals';

function buildSchema(
  configs: FieldConfig[],
): SchemaFn<Record<string, string | number | null | string[]>> {
  return (rootPath) => {
    for (const config of configs) {
      const applyRules = (path: typeof rootPath) => {
        const fieldPath = path[config.name];

        if (config.kind === 'array') {
          const arrayPath = fieldPath as unknown as SchemaPath<string[]>;
          if (config.itemRequired) {
            applyEach(arrayPath, (item) => required(item));
          }
          return;
        }

        if (config.required) required(fieldPath);

        if (config.kind === 'number') {
          const numberPath = fieldPath as unknown as SchemaPath<number | null>;
          if (config.min !== undefined) min(numberPath, config.min);
          if (config.max !== undefined) max(numberPath, config.max);
        }
      };

      if (config.when) {
        const {field, equals} = config.when;
        applyWhen(rootPath, ({valueOf}) => valueOf(rootPath[field]) === equals, applyRules);
      } else {
        applyRules(rootPath);
      }
    }
  };
}
```

Har bir shox ichidagi cast'lar ataylab qilingan "qochish yoʻllari" (escape hatch): siz kompilyatorning strukturaviy kafolatini atrofdagi `kind` tekshiruvi taʼminlaydigan runtime invariantiga almashtirasiz. Har bir cast `kind` blokiga cheklangan, shuning uchun bu taxmin lokal qoladi va uni tekshirish oson.

`array` turini ishlatadigan konfiguratsiya quyidagicha koʻrinadi:

```ts
const contactConfig: FieldConfig[] = [
  {kind: 'text', name: 'fullName', label: 'Full name', required: true},
  {kind: 'array', name: 'phoneNumbers', label: 'Phone numbers', itemRequired: true},
];
```

Massiv maydonini render qilish uchun uni `@for` bilan aylanib chiqing va foydalanuvchilarga model signalini yangilash orqali elementlar qoʻshish yoki olib tashlash imkonini bering. Iteratsiya massiv tuzilmasini koʻrishi uchun [`FieldTree`](api/forms/signals/FieldTree) qaytaradigan tiplangan accessor qoʻshing va modelni kengaytirish va qisqartirish metodlarini belgilang:

```ts
import {FieldTree} from '@angular/forms/signals';

// inside the component class
asArrayField(name: string): FieldTree<string[]> {
  return this.dynamicForm[name] as unknown as FieldTree<string[]>;
}

addItem(name: string) {
  this.model.update(current => ({
    ...current,
    [name]: [...(current[name] as string[]), ''],
  }));
}

removeItem(name: string, index: number) {
  this.model.update(current => ({
    ...current,
    [name]: (current[name] as string[]).filter((_, i) => i !== index),
  }));
}
```

`FieldTree<string[]>` iteratsiya qilinadigan obyekt, shuning uchun `@for` u boʻylab yura oladi; har bir element `[formField]`'ga bevosita mos keladigan `FieldTree<string>` boʻladi. Barg (leaf) maydonlar oʻrniga `Field<T>` accessor'laridan foydalanishi mumkin, chunki `Field<T>` — iteratsiyasiz chaqiriladigan signatura.

Shablonda massiv holatini (case) quyidagicha render qiling:

```angular-html
@case ('array') {
  <fieldset>
    <legend>{{ config.label }}</legend>
    @for (item of asArrayField(config.name); track item) {
      <input type="text" [formField]="item" />
      <button type="button" (click)="removeItem(config.name, $index)">Remove</button>
    }
    <button type="button" (click)="addItem(config.name)">Add</button>
  </fieldset>
}
```

`addItem()` metodi modelni kengaytiradi; forma massiv maydonlarini avtomatik qayta hosil qiladi. Yangi elementlar yangi validatsiya holati bilan boshlanadi. `removeItem()` metodi modelni filtrlaydi. Primitivlar massivlari [pozitsiya boʻyicha kuzatilgani](#tracking-item-identity) uchun maydon holati qiymatga emas, indeksga bogʻlangan: element olib tashlanganda keyingi qiymatlar oldingi pozitsiyalarga suriladi va ularning mavjud maydon holatini meros qilib oladi, oxirgi maydon esa tashlab yuboriladi.

### Element identifikatsiyasini kuzatish {#tracking-item-identity}

Signal Forms obyektlar massividagi har bir elementni uning identifikatsiyasi (identity) boʻyicha kuzatadi. Maʼlum pozitsiyadagi maydonga havolani saqlasangiz, bu havola pozitsiyaga emas, asosiy maʼlumotga ergashadi. Saqlangan havola orqali holatni oʻqish, maʼlumot koʻchib ketgan boʻlsa ham, oʻsha maʼlumotni qaytaradi:

```ts
const contactModel = signal([
  {name: 'Alice', phone: '555-0001'},
  {name: 'Bob', phone: '555-0002'},
]);

const contactForm = form(contactModel);

// Hold a reference to the field that's currently at index 0 (Alice).
const aliceField = contactForm[0];

// Swap the array items so Bob is at index 0, Alice at index 1.
contactModel.update(([alice, bob]) => [bob, alice]);

// The held reference still points to Alice's field, even after the swap.
console.log(aliceField().value().phone); // '555-0001' (Alice's number)
console.log(contactForm[0]().value().phone); // '555-0002' (Bob, now at index 0)
```

Bu identifikatsiya kuzatuvi, havola qilingan element massivda qolsa, saralash, qayta tartiblash yoki filtrlashda xatolarning oldini oladi. Saqlangan maydon havolalari massiv tartibi oʻzgarganda ham amal qilib qoladi; havola qilingan elementning oʻzi olib tashlansa, saqlangan havola egasiz qoladi.

Primitivlar massivlari uchun (yuqoridagi `phoneNumbers` misoli) Signal Forms elementlarni pozitsiya boʻyicha kuzatadi: 0-indeks doimo hozir 0-pozitsiyada turgan qiymatga ishora qiladi.

Bu yerda identifikatsiya maʼlumotlar bazasi kaliti kabi mantiqiy id boʻyicha emas, JavaScript obyekt havolasi boʻyicha aniqlanadi. Massivni yangi deserializatsiya qilingan obyektlar bilan almashtirsangiz (masalan, serverdan qayta yuklagandan keyin), har bir elementning `id`'si oʻzgarmagan boʻlsa ham maydon holati mantiqiy elementga ergashmaydi. Kafolat saralash, qayta tartiblash va filtrlash kabi xotiradagi amallarni qamrab oladi, maʼlumotlarni yangilashni emas.

## Konfiguratsiyani tekshirish {#validating-the-config}

Tashqi manbalardan kelgan konfiguratsiyalar forma yaratilishidan oldin tekshirilishi kerak. Ishonchsiz JSON'da bir nechta xato holatlari yashirinishi mumkin:

- Takrorlanuvchi `name` qiymatlari oldingi model yozuvlarini qayta yozadi va shablondagi `track config.name` ifodasini buzadi.
- Mavjud boʻlmagan maydonni koʻrsatuvchi `when` sharti shart birinchi marta hisoblanganda ish vaqtida xatoga uchraydi.
- `array` maydoni bilan taqqoslaydigan `when` shartining tenglik semantikasi belgilanmagan.
- Tipi havola qilingan maydon turiga mos kelmaydigan `when.equals` qiymati jimgina hech qachon mos kelmaydi va shartli xatti-harakatni qoida hech qachon faol boʻlmagandek yashiradi.

Bu toʻrttasini ham chegarada ushlang:

```ts
function validateConfigs(configs: FieldConfig[]): FieldConfig[] {
  const knownNames = new Set<string>();

  for (const config of configs) {
    if (knownNames.has(config.name)) {
      throw new Error(`Duplicate field name in config: "${config.name}"`);
    }
    knownNames.add(config.name);
  }

  for (const config of configs) {
    if (!config.when) continue;
    if (!knownNames.has(config.when.field)) {
      throw new Error(
        `Field "${config.name}" references unknown field "${config.when.field}" in its 'when' condition.`,
      );
    }
    const referenced = configs.find((c) => c.name === config.when!.field)!;
    if (referenced.kind === 'array') {
      throw new Error(
        `Field "${config.name}" cannot use 'when' to compare against array field "${config.when.field}".`,
      );
    }
    const expected = referenced.kind === 'text' ? 'string' : 'number';
    if (typeof config.when.equals !== expected) {
      throw new Error(
        `Field "${config.name}" compares ${referenced.kind} field "${config.when.field}" against a ${typeof config.when.equals} value; expected a ${expected}.`,
      );
    }
  }

  return configs;
}
```

Birinchi oʻtish yagonalikni taʼminlaydi; ikkinchi oʻtish har bir `when` shartini aylanib chiqib, havola qilingan maydon mavjudligini, massiv emasligini va toʻgʻri tipdagi qiymat bilan taqqoslanayotganini tasdiqlaydi. Muvaffaqiyatli boʻlganda funksiya konfiguratsiyalarni oʻzgarishsiz qaytaradi, shuning uchun u komponentda konfiguratsiyalarni saqlaydigan maydon initsializatori bilan yaxshi birikadi. Xatolar keyinroq formaning tushunarsiz notoʻgʻri ishlashi sifatida emas, ilovangiz va yuqori oqimdagi manba oʻrtasidagi chegarada yuzaga chiqadi.

## Formani dinamik render qilish {#rendering-the-form-dynamically}

Komponentda konfiguratsiyalar boʻylab aylanish uchun `@for`'dan va toʻgʻri input elementini tanlash uchun `kind` boʻyicha `@switch`'dan foydalaning:

```angular-ts
import {Component, signal} from '@angular/core';
import {Field, FieldTree, form, FormField, FormRoot} from '@angular/forms/signals';

@Component({
  selector: 'app-dynamic-form',
  imports: [FormField, FormRoot],
  template: `
    <form [formRoot]="dynamicForm">
      @for (config of configs; track config.name) {
        @switch (config.kind) {
          @case ('text') {
            <label>
              {{ config.label }}
              <input type="text" [formField]="asTextField(config.name)" />
            </label>
          }
          @case ('number') {
            <label>
              {{ config.label }}
              <input type="number" [formField]="asNumberField(config.name)" />
            </label>
          }
          @case ('array') {
            <fieldset>
              <legend>{{ config.label }}</legend>
              @for (item of asArrayField(config.name); track item; let i = $index) {
                <input type="text" [formField]="item" />
                <button type="button" (click)="removeItem(config.name, i)">Remove</button>
              }
              <button type="button" (click)="addItem(config.name)">Add</button>
            </fieldset>
          }
        }
      }
    </form>
  `,
})
export class DynamicForm {
  configs: FieldConfig[] = validateConfigs([
    {kind: 'text', name: 'fullName', label: 'Full Name', required: true},
    {kind: 'number', name: 'age', label: 'Age', required: true, min: 18, max: 120},
    {kind: 'array', name: 'phoneNumbers', label: 'Phone numbers', itemRequired: true},
  ]);

  model = signal(buildModel(this.configs));

  dynamicForm = form(this.model, buildSchema(this.configs));

  asTextField(name: string): Field<string> {
    // <input type="text"> requires Field<string>.
    return this.dynamicForm[name] as unknown as Field<string>;
  }

  asNumberField(name: string): Field<number | null> {
    // <input type="number"> requires Field<number | null>.
    return this.dynamicForm[name] as unknown as Field<number | null>;
  }

  asArrayField(name: string): FieldTree<string[]> {
    // FieldTree (not Field) so @for can iterate the array.
    return this.dynamicForm[name] as unknown as FieldTree<string[]>;
  }

  addItem(name: string) {
    this.model.update((current) => ({
      ...current,
      [name]: [...(current[name] as string[]), ''],
    }));
  }

  removeItem(name: string, index: number) {
    this.model.update((current) => ({
      ...current,
      [name]: (current[name] as string[]).filter((_, i) => i !== index),
    }));
  }
}
```

Shablon tip tekshiruvi `dynamicForm[name]`'ni mustaqil ifoda sifatida koʻradi, shuning uchun `config.kind` boʻyicha `@switch` toraytirishi indeksli murojaatga yetib bormaydi. Accessor'lar bu toraytirishni bogʻlash joyida cast sifatida qayta ifodalaydi, mos `kind` shoxi esa toraytirilgan tipning ish vaqtida toʻgʻri boʻlishini kafolatlaydi.

Model ham, sxema ham komponent yaratilishida bir xil `FieldConfig[]`'dan hosil qilingani uchun ular berilgan konfiguratsiya uchun bir-biridan uzoqlashib keta olmaydi. Yuqoridagi misol komponent yaratilganda konfiguratsiya sinxron tarzda mavjud deb hisoblaydi.

## Keyingi qadamlar {#next-steps}

JSON asosidagi formalar model va sxemasini bir xil `FieldConfig[]`'dan hosil qilish orqali bir-biriga mos holda saqlaydi. Ushbu qoʻllanmadagi har bir kengaytma (shartli qoidalar, takrorlanuvchi maydonlar) tipni kengaytiradi va bu moslikni saqlab qolgan holda `buildSchema()` ichiga aylantirish qadamini qoʻshadi. Konfiguratsiya qayerdan kelishi yoki qanday oʻsishidan qatʼi nazar, model va sxema bir-biriga bogʻlangan holda qoladi.

Signal Forms'ning boshqa jihatlarini yorituvchi tegishli qoʻllanmalar uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/schemas" title="Sxemalar va sxema kompozitsiyasi" />
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/form-logic" title="Forma mantigʻini qoʻshish" />
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
</docs-pill-row>

Batafsil API hujjatlari uchun qarang:

- [`form()`](api/forms/signals/form) - Model signalidan forma yaratish
- [`applyWhen()`](api/forms/signals/applyWhen) - Sxemani reaktiv holatga qarab shartli qoʻllash
- [`applyEach()`](api/forms/signals/applyEach) - Sxemani massiv maydonining har bir elementiga qoʻllash
- [`FieldTree`](api/forms/signals/FieldTree) - `form()` tomonidan taqdim etiladigan maydonlarning navigatsiya qilinadigan daraxti
- [`SchemaFn`](api/forms/signals/SchemaFn) - Sxema funksiyalari uchun tip signaturasi
