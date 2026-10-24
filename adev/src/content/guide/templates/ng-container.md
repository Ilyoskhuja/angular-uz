# Elementlarni ng-container bilan guruhlash

`<ng-container>` — bu Angular'dagi maxsus element boʻlib, DOM'da haqiqiy element render qilmasdan bir nechta elementni birga guruhlaydi yoki shablondagi joyni belgilaydi.

```angular-html
<!-- Component template -->
<section>
  <ng-container>
    <h3>User bio</h3>
    <p>Here's some info about the user</p>
  </ng-container>
</section>
```

```angular-html
<!-- Rendered DOM -->
<section>
  <h3>User bio</h3>
  <p>Here's some info about the user</p>
</section>
```

Shablonning bir qismiga xatti-harakat yoki konfiguratsiya qoʻshish uchun `<ng-container>`'ga direktivalar qoʻllashingiz mumkin.

Angular `<ng-container>`'ga qoʻllangan barcha atribut bogʻlashlari va hodisa tinglovchilarini, shu jumladan direktiva orqali qoʻllanganlarini ham, eʼtiborsiz qoldiradi.

## Dinamik kontentni koʻrsatish uchun `<ng-container>`'dan foydalanish {#using-ng-container-to-display-dynamic-contents}

`<ng-container>` dinamik kontentni render qilish uchun toʻldiruvchi (placeholder) vazifasini bajarishi mumkin.

### Komponentlarni render qilish {#rendering-components}

Komponentni `<ng-container>` joyiga dinamik ravishda render qilish uchun Angular'ning oʻrnatilgan `NgComponentOutlet` direktivasidan foydalanishingiz mumkin.

```angular-ts
@Component({
  template: `
    <h2>Your profile</h2>
    <ng-container [ngComponentOutlet]="profileComponent()" />
  `,
})
export class UserProfile {
  isAdmin = input(false);
  profileComponent = computed(() => (this.isAdmin() ? AdminProfile : BasicUserProfile));
}
```

Yuqoridagi misolda `NgComponentOutlet` direktivasi `<ng-container>` elementi joyida `AdminProfile` yoki `BasicUserProfile`'ni dinamik ravishda render qiladi.

### Shablon fragmentlarini render qilish {#rendering-template-fragments}

Shablon fragmentini `<ng-container>` joyiga dinamik ravishda render qilish uchun Angular'ning oʻrnatilgan `NgTemplateOutlet` direktivasidan foydalanishingiz mumkin.

```angular-ts
@Component({
  template: `
    <h2>Your profile</h2>
    <ng-container [ngTemplateOutlet]="profileTemplate()" />

    <ng-template #admin>This is the admin profile</ng-template>
    <ng-template #basic>This is the basic profile</ng-template>
  `,
})
export class UserProfile {
  isAdmin = input(false);
  adminTemplate = viewChild('admin', {read: TemplateRef});
  basicTemplate = viewChild('basic', {read: TemplateRef});
  profileTemplate = computed(() => (this.isAdmin() ? this.adminTemplate() : this.basicTemplate()));
}
```

Yuqoridagi misolda `ngTemplateOutlet` direktivasi `<ng-container>` elementi joyida ikkita shablon fragmentidan birini dinamik ravishda render qiladi.

`NgTemplateOutlet` haqida koʻproq maʼlumot uchun [NgTemplateOutlet API hujjatlari sahifasiga](/api/common/NgTemplateOutlet) qarang.

## `<ng-container>`'dan strukturaviy direktivalar bilan foydalanish {#using-ng-container-with-structural-directives}

Shuningdek, `<ng-container>` elementlariga strukturaviy direktivalar qoʻllashingiz ham mumkin. Bunga keng tarqalgan misollar — `ngIf` va `ngFor`.

```angular-html
<ng-container *ngIf="permissions == 'admin'">
  <h1>Admin Dashboard</h1>
  <admin-infographic />
</ng-container>

<ng-container *ngFor="let item of items; index as i; trackBy: trackByFn">
  <h2>{{ item.title }}</h2>
  <p>{{ item.description }}</p>
</ng-container>
```

## `<ng-container>`'dan inyeksiya uchun foydalanish {#using-ng-container-for-injection}

Angular'ning bogʻliqliklarni inyeksiya qilish tizimi haqida koʻproq maʼlumot uchun [Bogʻliqliklarni inyeksiya qilish qoʻllanmasiga](/guide/di) qarang.

`<ng-container>`'ga direktiva qoʻllaganingizda, avlod elementlar bu direktivani yoki direktiva taqdim etadigan har qanday narsani inyeksiya qila oladi. Shablonning maʼlum bir qismiga deklarativ tarzda qiymat taqdim etmoqchi boʻlganingizda bundan foydalaning.

```angular-ts
@Directive({
  selector: '[theme]',
})
export class Theme {
  // Create an input that accepts 'light' or 'dark`, defaulting to 'light'.
  mode = input<'light' | 'dark'>('light');
}
```

```angular-html
<ng-container theme="dark">
  <profile-pic />
  <user-bio />
</ng-container>
```

Yuqoridagi misolda `ProfilePic` va `UserBio` komponentlari `Theme` direktivasini inyeksiya qilib, uning `mode` qiymatiga qarab stillar qoʻllashi mumkin.
