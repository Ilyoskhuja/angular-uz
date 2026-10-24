# Bogʻliqliklarni inyeksiya qilishni tuzatish va muammolarni hal qilish

Bogʻliqliklarni inyeksiya qilish (DI) bilan bogʻliq muammolar odatda konfiguratsiya xatolari, qamrov (scope) muammolari yoki notoʻgʻri foydalanish namunalaridan kelib chiqadi. Bu qoʻllanma dasturchilar duch keladigan keng tarqalgan DI muammolarini aniqlash va hal qilishga yordam beradi.

## Keng tarqalgan xatolar va yechimlar {#common-pitfalls-and-solutions}

### Servislar kutilgan joyda mavjud emas {#services-not-available-where-expected}

Eng keng tarqalgan DI muammolaridan biri siz servisni inyeksiya qilmoqchi boʻlganingizda, lekin Angular uni joriy injector'da yoki hech qanday ota injector'da topa olmaganida yuzaga keladi. Bu odatda servis notoʻgʻri qamrovda taqdim etilganda yoki umuman taqdim etilmaganda sodir boʻladi.

#### Provider qamrovining mos kelmasligi {#provider-scope-mismatch}

Siz servisni komponentning `providers` massivida taqdim etganingizda, Angular oʻsha komponentning injector'ida nusxa yaratadi. Bu nusxa faqat oʻsha komponent va uning farzandlari uchun mavjud. Ota komponentlar va qoʻshni (sibling) komponentlar unga kira olmaydi, chunki ular boshqa injector'lardan foydalanadi.

```angular-ts {header: 'child-view.ts'}
import {Component} from '@angular/core';
import {DataStore} from './data-store';

@Component({
  selector: 'app-child',
  template: '<p>Child</p>',
  providers: [DataStore], // Only available in this component and its children
})
export class ChildView {}
```

```angular-ts {header: 'parent-view.ts'}
import {Component, inject} from '@angular/core';
import {DataStore} from './data-store';

@Component({
  selector: 'app-parent',
  template: '<app-child />',
})
export class ParentView {
  private dataService = inject(DataStore); // ERROR: Not available to parent
}
```

Angular ierarxiya boʻylab faqat yuqoriga qidiradi, hech qachon pastga emas. Ota komponentlar farzand komponentlarda taqdim etilgan servislarga kira olmaydi.

**Yechim:** Servisni yuqoriroq darajada (ilova yoki ota komponent darajasida) taqdim eting.

```ts {prefer}
import {Service} from '@angular/core';

@Service()
export class DataStore {
  // Available everywhere
}
```

TIP: `@Service` servislarni hamma joyda mavjud qiladi va tree-shaking imkonini beradi. Agar uni butun ilova qamroviga kiritishni istamasangiz, `autoProvided: false`'ni koʻrsating.

#### Servislar va lazy-load qilinadigan marshrutlar {#services-and-lazy-loaded-routes}

Siz servisni lazy-load qilinadigan marshrutning `providers` massivida taqdim etganingizda, Angular oʻsha marshrut uchun farzand injector yaratadi. Bu injector va uning servislari faqat marshrut yuklangandan keyin mavjud boʻladi. Ilovangizning darhol (eager) yuklanadigan qismlaridagi komponentlar bu servislarga kira olmaydi, chunki ular lazy-load qilinadigan injector yaratilishidan oldin mavjud boʻlgan boshqa injector'lardan foydalanadi.

```ts {header: 'feature.routes.ts'}
import {Routes} from '@angular/router';
import {FeatureClient} from './feature-client';

export const featureRoutes: Routes = [
  {
    path: 'feature',
    providers: [FeatureClient],
    loadComponent: () => import('./feature-view'),
  },
];
```

```angular-ts {header: 'eager-view.ts'}
import {Component, inject} from '@angular/core';
import {FeatureClient} from './feature-client';

@Component({
  selector: 'app-eager',
  template: '<p>Eager Component</p>',
})
export class EagerView {
  private featureService = inject(FeatureClient); // ERROR: Not available yet
}
```

Lazy-load qilinadigan marshrutlar faqat marshrut yuklangandan keyin mavjud boʻladigan farzand injector'lar yaratadi.

NOTE: Sukut boʻyicha marshrut injector'lari va ularning servislari marshrutdan chiqib ketilgandan keyin ham saqlanib qoladi. Ular ilova yopilmaguncha yoʻq qilinmaydi. Foydalanilmayotgan marshrut injector'larini avtomatik tozalash uchun [marshrut xatti-harakatini sozlash](guide/routing/customizing-route-behavior#automatic-cleanup-of-unused-route-injectors) boʻlimiga qarang.

**Yechim:** Lazy chegaralar boʻylab ulashilishi kerak boʻlgan servislar uchun `@Service`'dan foydalaning.

```ts {prefer, header: 'Provide at root for shared services'}
import {Service} from '@angular/core';

@Service()
export class FeatureClient {
  // Available everywhere, including before lazy load
}
```

Agar servis lazy-load qilinishi, lekin shu bilan birga darhol yuklanadigan komponentlar uchun ham mavjud boʻlishi kerak boʻlsa, uni faqat zarur joyda inyeksiya qiling va mavjudligini boshqarish uchun ixtiyoriy (optional) inyeksiyadan foydalaning.

### Singleton oʻrniga bir nechta nusxa {#multiple-instances-instead-of-singletons}

Siz bitta umumiy nusxa (singleton) kutasiz, lekin turli komponentlarda alohida nusxalar olasiz.

#### Root oʻrniga komponentda taqdim etish {#providing-in-component-instead-of-root}

Siz servisni komponentning `providers` massiviga qoʻshganingizda, Angular komponentning har bir nusxasi uchun oʻsha servisning yangi nusxasini yaratadi. Har bir komponent oʻzining alohida servis nusxasini oladi, yaʼni bir komponentdagi oʻzgarishlar boshqa komponentlardagi servis nusxasiga taʼsir qilmaydi. Ilovangiz boʻylab umumiy holatni istaganingizda bu koʻpincha kutilmagan holat boʻladi.

```angular-ts {avoid, header: 'Component-level provider creates multiple instances'}
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-profile',
  template: '<p>Profile</p>',
  providers: [UserClient], // Creates new instance per component!
})
export class UserProfile {
  private userService = inject(UserClient);
}

@Component({
  selector: 'app-settings',
  template: '<p>Settings</p>',
  providers: [UserClient], // Different instance!
})
export class UserSettings {
  private userService = inject(UserClient);
}
```

Har bir komponent oʻzining `UserClient` nusxasini oladi. Bir komponentdagi oʻzgarishlar boshqasiga taʼsir qilmaydi.

**Yechim:** Singleton'lar uchun `@Service`'dan foydalaning.

```ts {prefer, header: 'Root-level singleton'}
import {Service} from '@angular/core';

@Service()
export class UserClient {
  // Single instance shared across all components
}
```

#### Bir nechta nusxa ataylab kerak boʻlganda {#when-multiple-instances-are-intentional}

Baʼzan komponentga xos holat uchun har bir komponentga alohida nusxalar kerak boʻladi.

```angular-ts {header: 'Intentional: Component-scoped state'}
import {Injectable, signal} from '@angular/core';

@Injectable() // No providedIn - must be provided explicitly
export class FormStateStore {
  private formData = signal({});

  setData(data: any) {
    this.formData.set(data);
  }

  getData() {
    return this.formData();
  }
}

@Component({
  selector: 'app-user-form',
  template: '<form>...</form>',
  providers: [FormStateStore], // Each form gets its own state
})
export class UserForm {
  private formState = inject(FormStateStore);
}
```

Bu namuna quyidagilar uchun foydali:

- Forma holatini boshqarish (har bir forma izolyatsiyalangan holatga ega)
- Komponentga xos keshlash
- Ulashilmasligi kerak boʻlgan vaqtinchalik maʼlumotlar

### inject()'dan notoʻgʻri foydalanish {#incorrect-inject-usage}

`inject()` funksiyasi faqat klass konstruksiyasi va fabrika bajarilishi davomidagi muayyan kontekstlarda ishlaydi.

#### inject()'ni hayot sikli hook'larida ishlatish {#using-inject-in-lifecycle-hooks}

Siz `inject()` funksiyasini `ngOnInit()`, `ngAfterViewInit()` yoki `ngOnDestroy()` kabi hayot sikli hook'lari ichida chaqirganingizda, Angular xato chiqaradi, chunki bu metodlar inyeksiya kontekstidan tashqarida ishlaydi. Inyeksiya konteksti faqat klass konstruksiyasining sinxron bajarilishi davomida mavjud boʻladi, bu esa hayot sikli hook'lari chaqirilishidan oldin sodir boʻladi.

```angular-ts {avoid, header: 'inject() in ngOnInit'}
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-profile',
  template: '<p>User: {{userName}}</p>',
})
export class UserProfile {
  userName = '';

  ngOnInit() {
    const userService = inject(UserClient); // ERROR: Not an injection context
    this.userName = userService.getUser().name;
  }
}
```

**Yechim:** Bogʻliqliklarni maydon initsializatorlarida ushlab oling va qiymatlarni shu yerda hosil qiling.

```angular-ts {prefer, header: 'Derive values in field initializers'}
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-profile',
  template: '<p>User: {{userName}}</p>',
})
export class UserProfile {
  private userService = inject(UserClient);
  userName = this.userService.getUser().name;
}
```

#### Kechiktirilgan inyeksiya uchun Injector'dan foydalanish {#using-the-injector-for-deferred-injection}

Servislarni inyeksiya kontekstidan tashqarida olish kerak boʻlganda, ushlab olingan `Injector`'dan bevosita `injector.get()` orqali foydalaning:

```angular-ts
import {Component, inject, Injector} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-profile',
  template: '<button (click)="delayedLoad()">Load Later</button>',
})
export class UserProfile {
  private injector = inject(Injector);

  delayedLoad() {
    setTimeout(() => {
      const userService = this.injector.get(UserClient);
      console.log(userService.getUser());
    }, 1000);
  }
}
```

#### Callback'lar uchun runInInjectionContext'dan foydalanish {#using-runininjectioncontext-for-callbacks}

**Boshqa kod** `inject()`'ni chaqira olishini taʼminlash kerak boʻlganda `runInInjectionContext()`'dan foydalaning. Bu bogʻliqliklarni inyeksiya qilishdan foydalanishi mumkin boʻlgan callback'larni qabul qilganda foydali:

```angular-ts
import {Component, inject, Injector, input, runInInjectionContext} from '@angular/core';

@Component({
  selector: 'app-data-loader',
  template: '<button (click)="load()">Load</button>',
})
export class DataLoader {
  private injector = inject(Injector);
  onLoad = input<() => void>();

  load() {
    const callback = this.onLoad();
    if (callback) {
      // Enable the callback to use inject()
      runInInjectionContext(this.injector, callback);
    }
  }
}
```

`runInInjectionContext()` funksiyasi vaqtinchalik inyeksiya konteksti yaratadi va callback ichidagi kodga `inject()`'ni chaqirish imkonini beradi.

IMPORTANT: Iloji boricha bogʻliqliklarni doimo klass darajasida ushlab oling. Oddiy kechiktirilgan olish uchun `injector.get()`'dan, `runInInjectionContext()`'dan esa faqat tashqi kod `inject()`'ni chaqirishi kerak boʻlganda foydalaning.

TIP: Kodingiz toʻgʻri inyeksiya kontekstida ishlayotganini tekshirish uchun `assertInInjectionContext()`'dan foydalaning. Bu `inject()`'ni chaqiruvchi qayta ishlatiladigan funksiyalar yaratishda foydali. Tafsilotlar uchun [Kontekstni tasdiqlash](guide/di/dependency-injection-context#asserts-the-context) boʻlimiga qarang.

### providers va viewProviders chalkashligi {#providers-vs-viewproviders-confusion}

`providers` va `viewProviders` oʻrtasidagi farq kontent proyeksiyasi stsenariylariga taʼsir qiladi.

#### Farqni tushunish {#understanding-the-difference}

**providers:** Komponent shabloni uchun HAM, komponentga proyeksiya qilingan har qanday kontent (ng-content) uchun HAM mavjud.

**viewProviders:** Faqat komponent shabloni uchun mavjud, proyeksiya qilingan kontent uchun mavjud EMAS.

```angular-ts {header: 'parent-view.ts'}
import {Component, inject} from '@angular/core';
import {ThemeStore} from './theme-store';

@Component({
  selector: 'app-parent',
  template: `
    <div>
      <p>Theme: {{ themeService.theme() }}</p>
      <ng-content />
    </div>
  `,
  providers: [ThemeStore], // Available to content children
})
export class ParentView {
  protected themeService = inject(ThemeStore);
}

@Component({
  selector: 'app-parent-view',
  template: `
    <div>
      <p>Theme: {{ themeService.theme() }}</p>
      <ng-content />
    </div>
  `,
  viewProviders: [ThemeStore], // NOT available to content children
})
export class ParentViewOnly {
  protected themeService = inject(ThemeStore);
}
```

```angular-ts {header: 'child-view.ts'}
import {Component, inject} from '@angular/core';
import {ThemeStore} from './theme-store';

@Component({
  selector: 'app-child',
  template: '<p>Child theme: {{theme()}}</p>',
})
export class ChildView {
  private themeService = inject(ThemeStore, {optional: true});
  theme = () => this.themeService?.theme() ?? 'none';
}
```

```angular-ts {header: 'app.ts'}
@Component({
  selector: 'app-root',
  template: `
    <app-parent>
      <app-child />
      <!-- Can access ThemeStore -->
    </app-parent>

    <app-parent-view>
      <app-child />
      <!-- Cannot access ThemeStore -->
    </app-parent-view>
  `,
})
export class App {}
```

**`app-parent` ichiga proyeksiya qilinganda:** Farzand komponent `ThemeStore`'ni inyeksiya qila oladi, chunki `providers` uni proyeksiya qilingan kontent uchun mavjud qiladi.

**`app-parent-view` ichiga proyeksiya qilinganda:** Farzand komponent `ThemeStore`'ni inyeksiya qila olmaydi, chunki `viewProviders` uni faqat ota komponentning shabloni bilan cheklaydi.

#### providers va viewProviders oʻrtasida tanlov {#choosing-between-providers-and-viewproviders}

`providers`'dan quyidagi hollarda foydalaning:

- Servis proyeksiya qilingan kontent uchun mavjud boʻlishi kerak boʻlsa
- Kontent farzandlari servisga kirishini istasangiz
- Umumiy maqsadli servislarni taqdim etayotgan boʻlsangiz

`viewProviders`'dan quyidagi hollarda foydalaning:

- Servis faqat komponentingiz shabloni uchun mavjud boʻlishi kerak boʻlsa
- Realizatsiya tafsilotlarini proyeksiya qilingan kontentdan yashirishni istasangiz
- Tashqariga chiqib ketmasligi kerak boʻlgan ichki servislarni taqdim etayotgan boʻlsangiz

**Sukut boʻyicha tavsiya:** Kirishni `viewProviders` bilan cheklash uchun aniq sababingiz boʻlmasa, `providers`'dan foydalaning.

### InjectionToken bilan bogʻliq muammolar {#injectiontoken-issues}

Klass boʻlmagan bogʻliqliklar uchun `InjectionToken`'dan foydalanganda dasturchilar koʻpincha token identifikatsiyasi, tip xavfsizligi va provider konfiguratsiyasi bilan bogʻliq muammolarga duch keladi. Bu muammolar odatda JavaScript obyekt identifikatsiyasini qanday boshqarishi va TypeScript tiplarni qanday aniqlashidan kelib chiqadi.

#### Token identifikatsiyasi chalkashligi {#token-identity-confusion}

Siz yangi `InjectionToken` nusxasini yaratganingizda, JavaScript xotirada noyob obyekt yaratadi. Hatto siz aynan bir xil tavsif satri bilan boshqa `InjectionToken` yaratsangiz ham, bu butunlay boshqa obyekt boʻladi. Angular provider'larni inyeksiya nuqtalari bilan moslashtirish uchun token obyektining identifikatsiyasidan (tavsifidan emas) foydalanadi, shuning uchun tavsifi bir xil, lekin obyekt identifikatsiyasi boshqa tokenlar bir-birining qiymatlariga kira olmaydi.

```ts {header: 'config.token.ts'}
import {InjectionToken} from '@angular/core';

export interface AppConfig {
  apiUrl: string;
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app config');
```

```ts {header: 'app.config.ts'}
import {APP_CONFIG} from './config.token';

export const appConfig: AppConfig = {
  apiUrl: 'https://api.example.com',
};

bootstrapApplication(App, {
  providers: [{provide: APP_CONFIG, useValue: appConfig}],
});
```

```angular-ts {avoid, header: 'feature-view.ts'}
// Creating new token with same description
import {InjectionToken, inject} from '@angular/core';
import {AppConfig} from './config.token';

const APP_CONFIG = new InjectionToken<AppConfig>('app config');

@Component({
  selector: 'app-feature',
  template: '<p>Feature</p>',
})
export class FeatureView {
  private config = inject(APP_CONFIG); // ERROR: Different token instance!
}
```

Ikkala tokenning tavsifi `'app config'` boʻlsa ham, ular boshqa-boshqa obyektlar. Angular tokenlarni tavsif boʻyicha emas, havola (reference) boʻyicha solishtiradi.

**Yechim:** Aynan oʻsha token nusxasini import qiling.

```angular-ts {prefer, header: 'feature-view.ts'}
import {inject} from '@angular/core';
import {APP_CONFIG, AppConfig} from './config.token';

@Component({
  selector: 'app-feature',
  template: '<p>API: {{config.apiUrl}}</p>',
})
export class FeatureView {
  protected config = inject(APP_CONFIG); // Works: Same token instance
}
```

TIP: Tokenlarni doimo umumiy fayldan eksport qiling va ular kerak boʻlgan har bir joyga import qiling. Hech qachon bir xil tavsifli bir nechta `InjectionToken` nusxasini yaratmang.

#### Interfeyslarni inyeksiya qilishga urinish {#trying-to-inject-interfaces}

Siz TypeScript interfeysini aniqlaganingizda, u faqat kompilyatsiya vaqtida tip tekshiruvi uchun mavjud boʻladi. TypeScript JavaScript'ga kompilyatsiya qilganda barcha interfeys taʼriflarini oʻchirib tashlaydi, shuning uchun ishga tushirish vaqtida Angular inyeksiya tokeni sifatida ishlata oladigan obyekt boʻlmaydi. Agar siz interfeys tipini inyeksiya qilishga urinsangiz, Angular'da provider konfiguratsiyasi bilan moslashtiradigan hech narsa boʻlmaydi.

```angular-ts {avoid, header: "Can't inject interface"}
interface UserConfig {
  name: string;
  email: string;
}

@Component({
  selector: 'app-profile',
  template: '<p>Profile</p>',
})
export class UserProfile {
  // ERROR: Interfaces don't exist at runtime
  constructor(private config: UserConfig) {}
}
```

**Yechim:** Interfeys tiplari uchun `InjectionToken`'dan foydalaning.

```angular-ts {prefer, header: 'Use InjectionToken for interfaces'}
import {InjectionToken, inject} from '@angular/core';

interface UserConfig {
  name: string;
  email: string;
}

export const USER_CONFIG = new InjectionToken<UserConfig>('user configuration');

// Provide the configuration
bootstrapApplication(App, {
  providers: [
    {
      provide: USER_CONFIG,
      useValue: {name: 'Alice', email: 'alice@example.com'},
    },
  ],
});

// Inject using the token
@Component({
  selector: 'app-profile',
  template: '<p>User: {{config.name}}</p>',
})
export class UserProfile {
  protected config = inject(USER_CONFIG);
}
```

`InjectionToken` ishga tushirish vaqtida mavjud boʻladi va inyeksiya uchun ishlatilishi mumkin, `UserConfig` interfeysi esa ishlab chiqish davomida tip xavfsizligini taʼminlaydi.

### Siklik bogʻliqliklar {#circular-dependencies}

Siklik bogʻliqliklar servislar bir-birini inyeksiya qilganda yuzaga keladi va Angular hal qila olmaydigan sikl hosil qiladi. Batafsil tushuntirishlar va kod misollari uchun [NG0200: Siklik bogʻliqlik](errors/NG0200) boʻlimiga qarang.

**Hal qilish strategiyalari** (afzallik tartibida):

1. **Qayta tuzish** - Umumiy mantiqni uchinchi servisga ajratib, siklni buzing
2. **Hodisalardan foydalanish** - Bevosita bogʻliqliklarni hodisaga asoslangan aloqa bilan almashtiring (masalan, `Subject`)
3. **Lazy inyeksiya** - Bitta bogʻliqlikni kechiktirish uchun `Injector.get()`'dan foydalaning (oxirgi chora)

NOTE: Servislarning siklik bogʻliqliklari uchun `forwardRef()`'dan foydalanmang — u faqat standalone komponent konfiguratsiyalaridagi siklik importlarni hal qiladi.

## Bogʻliqliklarni hal qilish jarayonini tuzatish {#debugging-dependency-resolution}

### Hal qilish jarayonini tushunish {#understanding-the-resolution-process}

Angular bogʻliqliklarni injector ierarxiyasi boʻylab yuqoriga koʻtarilib hal qiladi. `NullInjectorError` yuzaga kelganda, bu qidirish tartibini tushunish yetishmayotgan provider'ni qayerga qoʻshish kerakligini aniqlashga yordam beradi.

Angular quyidagi tartibda qidiradi:

1. **Element injector** - Joriy komponent yoki direktiva
2. **Ota element injector'lari** - DOM daraxti boʻylab ota komponentlar orqali yuqoriga
3. **Environment injector** - Marshrut yoki ilova injector'i
4. **NullInjector** - Topilmasa, `NullInjectorError` chiqaradi

`NullInjectorError`'ni koʻrganingizda, servis komponent kira oladigan hech bir darajada taqdim etilmagan boʻladi. Quyidagilarni tekshiring:

- Servis `@Service()`'ga ega, yoki
- Servis `@Injectable({providedIn: 'root'})`'ga ega, yoki
- Servis komponent yeta oladigan `providers` massivida joylashgan

Bu qidirish xatti-harakatini `self`, `skipSelf`, `host` va `optional` kabi hal qilish modifikatorlari bilan oʻzgartirishingiz mumkin. Hal qilish qoidalari va modifikatorlarning toʻliq qamrovi uchun [Ierarxik injector'lar qoʻllanmasiga](guide/di/hierarchical-dependency-injection) qarang.

### Angular DevTools'dan foydalanish {#using-angular-devtools}

Angular DevTools butun injector ierarxiyasini vizuallashtiruvchi va har bir darajada qaysi provider'lar mavjudligini koʻrsatuvchi injector daraxti inspektorini oʻz ichiga oladi. Oʻrnatish va umumiy foydalanish uchun [Angular DevTools injector hujjatlariga](tools/devtools/injectors) qarang.

DI muammolarini tuzatishda quyidagi savollarga javob berish uchun DevTools'dan foydalaning:

- **Servis taqdim etilganmi?** Inyeksiya qila olmayotgan komponentni tanlang va servis Injector boʻlimida koʻrinishini tekshiring.
- **Qaysi darajada?** Servis aslida qayerda (komponent, marshrut yoki ilova darajasida) taqdim etilganini topish uchun komponent daraxti boʻylab yuqoriga koʻtariling.
- **Bir nechta nusxa?** Agar singleton servis bir nechta komponent injector'ida koʻrinsa, u `@Service` yoki `providedIn: 'root'` oʻrniga komponentlarning `providers` massivlarida taqdim etilgan boʻlishi ehtimoli katta.

Agar servis hech bir injector'da umuman koʻrinmasa, u `@Service` dekoratoriga ega ekanligini yoki `providers` massivida roʻyxatga olinganligini tekshiring.

### Inyeksiyani loglash va kuzatish {#logging-and-tracing-injection}

DevTools yetarli boʻlmaganda, inyeksiya xatti-harakatini kuzatish uchun loglashdan foydalaning.

#### Servis yaratilishini loglash {#logging-service-creation}

Servislar qachon yaratilishini koʻrish uchun servis konstruktorlariga konsol loglarini qoʻshing.

```ts
import {Service} from '@angular/core';

@Service()
export class UserClient {
  constructor() {
    console.log('UserClient created');
    console.trace(); // Shows call stack
  }

  getUser() {
    return {name: 'Alice'};
  }
}
```

Servis yaratilganda siz log xabarini va inyeksiya qayerda sodir boʻlganini koʻrsatuvchi stek izini (stack trace) koʻrasiz.

**Nimaga eʼtibor berish kerak:**

- Konstruktor necha marta chaqirilgan? (singleton'lar uchun bir marta boʻlishi kerak)
- Kodning qayerida inyeksiya qilinmoqda? (stek izini tekshiring)
- U kutilgan vaqtda yaratilganmi? (ilova ishga tushganda yoki lazy)

#### Servis mavjudligini tekshirish {#checking-service-availability}

Servis mavjudligini aniqlash uchun loglash bilan birga ixtiyoriy inyeksiyadan foydalaning.

```angular-ts
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-debug',
  template: '<p>Debug Component</p>',
})
export class DebugView {
  private userService = inject(UserClient, {optional: true});

  constructor() {
    if (this.userService) {
      console.log('UserClient available:', this.userService);
    } else {
      console.warn('UserClient NOT available');
      console.trace(); // Shows where we tried to inject
    }
  }
}
```

Bu namuna ilovani ishdan chiqarmasdan servis mavjudligini tekshirishga yordam beradi.

#### Hal qilish modifikatorlarini loglash {#logging-resolution-modifiers}

Loglash yordamida turli hal qilish strategiyalarini sinab koʻring.

```angular-ts
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-debug',
  template: '<p>Debug Component</p>',
  providers: [UserClient],
})
export class DebugView {
  // Try to get local instance
  private localService = inject(UserClient, {self: true, optional: true});

  // Try to get parent instance
  private parentService = inject(UserClient, {
    skipSelf: true,
    optional: true,
  });

  constructor() {
    console.log('Local instance:', this.localService);
    console.log('Parent instance:', this.parentService);
    console.log('Same instance?', this.localService === this.parentService);
  }
}
```

Bu sizga turli injector darajalarida qaysi nusxalar mavjudligini koʻrsatadi.

### Tuzatish ish jarayoni {#debugging-workflow}

DI ishlamay qolganda, quyidagi tizimli yondashuvga amal qiling:

**1-qadam: Xato xabarini oʻqing**

- Xato kodini aniqlang (NG0200, NG0203 va h.k.)
- Bogʻliqlik yoʻlini oʻqing
- Qaysi token muvaffaqiyatsiz boʻlganini qayd eting

**2-qadam: Asosiy narsalarni tekshiring**

- Servis `@Service` yoki `@Injectable()`'ga egami?
- Agar `@Injectable`'dan foydalansangiz, `providedIn` toʻgʻri oʻrnatilganmi?
- Importlar toʻgʻrimi?
- Fayl kompilyatsiyaga kiritilganmi?

**3-qadam: Inyeksiya kontekstini tekshiring**

- `inject()` toʻgʻri kontekstda chaqirilganmi?
- Asinxron muammolarni tekshiring (await, setTimeout, promise'lar)
- Vaqtni tekshiring (yoʻq qilingandan keyin emas)

**4-qadam: Tuzatish vositalaridan foydalaning**

- Angular DevTools'ni oching
- Injector ierarxiyasini tekshiring
- Konstruktorlarga konsol loglarini qoʻshing
- Mavjudlikni sinash uchun ixtiyoriy inyeksiyadan foydalaning

**5-qadam: Soddalashtiring va izolyatsiya qiling**

- Bogʻliqliklarni birma-bir olib tashlang
- Minimal komponentda sinab koʻring
- Har bir injector darajasini alohida tekshiring
- Takrorlanish holatini (reproduction case) yarating

## DI xatolari boʻyicha maʼlumotnoma {#di-error-reference}

Bu boʻlim siz duch kelishingiz mumkin boʻlgan muayyan Angular DI xato kodlari haqida batafsil maʼlumot beradi. Konsolingizda bu xatolarni koʻrganingizda undan maʼlumotnoma sifatida foydalaning.

### NullInjectorError: No provider for [Service]

**Xato kodi:** [NG0201](errors/NG0201)

Bu xato Angular injector ierarxiyasida token uchun provider topa olmaganda yuzaga keladi. Xato xabari inyeksiya qayerda amalga oshirilganini koʻrsatuvchi bogʻliqlik yoʻlini oʻz ichiga oladi.

```
NG0201: No provider found for `UserClient`. Path: AuthClient -> UserClient.
```

Bogʻliqlik yoʻli `AuthClient` `UserClient`'ni inyeksiya qilishga uringanini, lekin provider topilmaganini koʻrsatadi.

#### `@Service ` yoki `@Injectable` dekoratorining yoʻqligi {#missing-the-service--or-injectable-decorator}

Eng keng tarqalgan sabab — servis klassida `@Service` yoki `@Injectable()` dekoratorini unutish.

```ts {avoid, header: 'Missing decorator'}
export class UserClient {
  getUser() {
    return {name: 'Alice'};
  }
}
```

Angular bogʻliqliklarni inyeksiya qilish uchun zarur metamaʼlumotlarni yaratish uchun `@Service()` dekoratorini talab qiladi.

```ts {prefer, header: 'Include @Service'}
import {Service} from '@angular/core';

@Service()
export class UserClient {
  getUser() {
    return {name: 'Alice'};
  }
}
```

NOTE: Argumentsiz konstruktorga ega klasslar `@Service()`'siz ham ishlashi mumkin, lekin bu tavsiya etilmaydi. Izchillik uchun va keyinroq bogʻliqliklar qoʻshganda muammolardan qochish uchun dekoratorni doimo qoʻshing.

#### providedIn konfiguratsiyasining yoʻqligi {#missing-providedin-configuration}

Servis `@Injectable()`'ga ega boʻlishi, lekin qayerda taqdim etilishi kerakligini koʻrsatmasligi mumkin.

```ts {avoid, header: 'No providedIn specified'}
import {Injectable} from '@angular/core';

@Injectable()
export class UserClient {
  getUser() {
    return {name: 'Alice'};
  }
}
```

Servisni butun ilovangiz boʻylab mavjud qilish uchun `@Service` dekoratoridan foydalaning.

```ts {prefer, header: 'Specify providedIn'}
import {Service} from '@angular/core';

@Service()
export class UserClient {
  getUser() {
    return {name: 'Alice'};
  }
}
```

`@Service` dekoratori servisni butun ilova boʻylab mavjud qiladi va tree-shaking imkonini beradi (servis hech qachon inyeksiya qilinmasa, bundle'dan olib tashlanadi).

#### Standalone komponentda importlarning yoʻqligi {#standalone-component-missing-imports}

Angular v20+ da standalone komponentlar bilan siz har bir komponentda bogʻliqliklarni aniq import qilishingiz yoki taqdim etishingiz kerak.

```angular-ts {avoid, header: 'Missing service import'}
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-profile',
  template: '<p>User: {{user.name}}</p>',
})
export class UserProfile {
  private userService = inject(UserClient); // ERROR: No provider
  user = this.userService.getUser();
}
```

Servis `@Service`'dan foydalanishini taʼminlang yoki uni komponentning `providers` massiviga qoʻshing.

```angular-ts {prefer, header: 'Service uses providedIn: root'}
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-profile',
  template: '<p>User: {{user.name}}</p>',
})
export class UserProfile {
  private userService = inject(UserClient); // Works: providedIn: 'root'
  user = this.userService.getUser();
}
```

#### Bogʻliqlik yoʻli yordamida tuzatish {#debugging-with-the-dependency-path}

Xato xabaridagi bogʻliqlik yoʻli muvaffaqiyatsizlikka olib kelgan inyeksiyalar zanjirini koʻrsatadi.

```
NG0201: No provider found for `LoggerStore`. Path: DataStore -> ApiClient -> LoggerStore.
```

Bu yoʻl sizga quyidagilarni aytadi:

1. `DataStore` `ApiClient`'ni inyeksiya qildi
2. `ApiClient` `LoggerStore`'ni inyeksiya qilishga urindi
3. `LoggerStore` uchun provider topilmadi

Tekshiruvni zanjirning oxiridan (`LoggerStore`) boshlang va u toʻgʻri konfiguratsiyaga ega ekanligini tekshiring.

#### Ixtiyoriy inyeksiya yordamida provider mavjudligini tekshirish {#checking-provider-availability-with-optional-injection}

Xato chiqarmasdan provider mavjudligini tekshirish uchun ixtiyoriy inyeksiyadan foydalaning.

```angular-ts
import {Component, inject} from '@angular/core';
import {UserClient} from './user-client';

@Component({
  selector: 'app-debug',
  template: '<p>Service available: {{serviceAvailable}}</p>',
})
export class DebugView {
  private userService = inject(UserClient, {optional: true});
  serviceAvailable = this.userService !== null;
}
```

Ixtiyoriy inyeksiya provider topilmasa `null` qaytaradi va bu sizga yoʻqlikni toʻgʻri boshqarish imkonini beradi.

### NG0203: inject() must be called from an injection context

**Xato kodi:** NG0203

Bu xato siz `inject()`'ni toʻgʻri inyeksiya kontekstidan tashqarida chaqirganingizda yuzaga keladi. Angular `inject()`'ning klass konstruksiyasi yoki fabrika bajarilishi davomida sinxron chaqirilishini talab qiladi.

```
NG0203: The `UserClient` token injection failed. `inject()` function must
be called from an injection context such as a constructor, a factory
function, a field initializer, or a function used with
`runInInjectionContext`.
```

#### Toʻgʻri inyeksiya kontekstlari {#valid-injection-contexts}

Angular `inject()`'ni quyidagi joylarda ishlatishga ruxsat beradi:

1. **Klass maydoni initsializatorlari**

   ```angular-ts
   import {Component, inject} from '@angular/core';
   import {UserClient} from './user-client';

   @Component({
     selector: 'app-profile',
     template: '<p>User: {{user.name}}</p>',
   })
   export class UserProfile {
     private userService = inject(UserClient); // Valid
     user = this.userService.getUser();
   }
   ```

2. **Klass konstruktori**

   ```angular-ts
   import {Component, inject} from '@angular/core';
   import {UserClient} from './user-client';

   @Component({
     selector: 'app-profile',
     template: '<p>User: {{user.name}}</p>',
   })
   export class UserProfile {
     private userService: UserClient;
     user: ReturnType<UserClient['getUser']>;

     constructor() {
       this.userService = inject(UserClient); // Valid
       this.user = this.userService.getUser();
     }
   }
   ```

3. **Provider fabrika funksiyalari**

   ```ts
   import {inject, InjectionToken} from '@angular/core';
   import {UserClient} from './user-client';

   export const GREETING = new InjectionToken<string>('greeting', {
     factory() {
       const userService = inject(UserClient); // Valid
       const user = userService.getUser();
       return `Hello, ${user.name}`;
     },
   });
   ```

4. **runInInjectionContext() ichida**

   ```angular-ts
   import {Component, inject, Injector, runInInjectionContext} from '@angular/core';
   import {UserClient} from './user-client';

   @Component({
     selector: 'app-profile',
     template: '<button (click)="loadUser()">Load User</button>',
   })
   export class UserProfile {
     private injector = inject(Injector);

     loadUser() {
       runInInjectionContext(this.injector, () => {
         const userService = inject(UserClient); // Valid
         console.log(userService.getUser());
       });
     }
   }
   ```

`inject()` ishlaydigan boshqa inyeksiya kontekstlari quyidagilarni oʻz ichiga oladi:

- [provideAppInitializer](api/core/provideAppInitializer)
- [provideEnvironmentInitializer](api/core/provideEnvironmentInitializer)
- Funksional [marshrut himoyachilari (guards)](guide/routing/route-guards)
- Funksional [maʼlumot resolver'lari](guide/routing/data-resolvers)
- Marshrut [resurslari](guide/routing/data-fetching-with-resources)

#### Bu xato qachon yuzaga keladi {#when-this-error-occurs}

Bu xato quyidagi hollarda yuzaga keladi:

- `inject()`'ni hayot sikli hook'larida (`ngOnInit`, `ngAfterViewInit` va h.k.) chaqirganda
- `inject()`'ni asinxron funksiyalarda `await`'dan keyin chaqirganda
- `inject()`'ni callback'larda (`setTimeout`, `Promise.then()` va h.k.) chaqirganda
- `inject()`'ni klass konstruksiyasi bosqichidan tashqarida chaqirganda

Batafsil misollar va yechimlar uchun "inject()'dan notoʻgʻri foydalanish" boʻlimiga qarang.

#### Yechimlar va chetlab oʻtish usullari {#solutions-and-workarounds}

**1-yechim:** Bogʻliqliklarni maydon initsializatorlarida ushlab oling (eng keng tarqalgan)

```ts
private userService = inject(UserClient) // Capture at class level
```

**2-yechim:** Callback'lar uchun `runInInjectionContext()`'dan foydalaning

```ts
private injector = inject(Injector)

someCallback() {
  runInInjectionContext(this.injector, () => {
    const service = inject(MyClient)
  })
}
```

**3-yechim:** Bogʻliqliklarni inyeksiya qilish oʻrniga ularni parametr sifatida uzating

```ts
// Instead of injecting inside a callback
setTimeout(() => {
  const service = inject(MyClient) // ERROR
}, 1000)

// Capture first, then use
private service = inject(MyClient)

setTimeout(() => {
  this.service.doSomething() // Use captured reference
}, 1000)
```

### NG0200: Circular dependency detected

**Xato kodi:** NG0200

Bu xato ikki yoki undan ortiq servis bir-biriga bogʻliq boʻlib, Angular hal qila olmaydigan siklik bogʻliqlik hosil qilganda yuzaga keladi.

```
NG0200: Circular dependency detected for `AuthClient`. Path: AuthClient -> UserClient -> AuthClient.
```

Bogʻliqlik yoʻli siklni koʻrsatadi: `AuthClient` `UserClient`'ga bogʻliq, u esa oʻz navbatida `AuthClient`'ga bogʻliq.

#### Xatoni tushunish {#understanding-the-error}

Angular servis nusxalarini ularning konstruktorlarini chaqirish va bogʻliqliklarni inyeksiya qilish orqali yaratadi. Servislar bir-biriga siklik tarzda bogʻliq boʻlganda, Angular qaysi birini birinchi yaratish kerakligini aniqlay olmaydi.

#### Keng tarqalgan sabablar {#common-causes}

- Bevosita siklik bogʻliqlik (A servis → B servis → A servis)
- Bilvosita siklik bogʻliqlik (A servis → B servis → C servis → A servis)
- Servis bogʻliqliklariga ham ega boʻlgan modul fayllaridagi import sikllari

#### Hal qilish strategiyalari {#resolution-strategies}

Batafsil misollar va yechimlar uchun "Siklik bogʻliqliklar" boʻlimiga qarang:

1. **Qayta tuzish** - Umumiy mantiqni uchinchi servisga ajrating (tavsiya etiladi)
2. **Hodisalardan foydalanish** - Bevosita bogʻliqliklarni hodisaga asoslangan aloqa bilan almashtiring
3. **Lazy inyeksiya** - Bitta bogʻliqlikni kechiktirish uchun `Injector.get()`'dan foydalaning (oxirgi chora)

Servislarning siklik bogʻliqliklari uchun `forwardRef()`'dan foydalanmang. U faqat komponent konfiguratsiyalaridagi siklik importlarni hal qiladi.

### Boshqa DI xato kodlari {#other-di-error-codes}

Bu xatolar boʻyicha batafsil tushuntirishlar va yechimlar uchun [Angular xatolar maʼlumotnomasiga](errors) qarang:

| Xato kodi               | Tavsif                                                                                              |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| [NG0204](errors/NG0204) | Barcha parametrlarni hal qilib boʻlmadi - `@Injectable()` dekoratori yoʻq                            |
| [NG0205](errors/NG0205) | Injector allaqachon yoʻq qilingan - komponent yoʻq qilingandan keyin servislarga murojaat qilish    |
| [NG0207](errors/NG0207) | EnvironmentProviders notoʻgʻri kontekstda - `provideHttpClient()`'ni komponent provider'larida ishlatish |

## Keyingi qadamlar {#next-steps}

DI xatolariga duch kelganingizda quyidagilarni yodda tuting:

1. Xato xabari va bogʻliqlik yoʻlini diqqat bilan oʻqing
2. Asosiy konfiguratsiyani tekshiring (dekoratorlar, `providedIn`, importlar)
3. Inyeksiya konteksti va vaqtni tekshiring
4. Tekshirish uchun DevTools va loglashdan foydalaning
5. Muammoni soddalashtiring va izolyatsiya qiling

Bogʻliqliklarni inyeksiya qilishning muayyan mavzularini chuqurroq tushunish uchun quyidagilarni koʻrib chiqing:

- [Bogʻliqliklarni inyeksiya qilishni tushunish](guide/di) - DI'ning asosiy tushunchalari va namunalari
- [Ierarxik bogʻliqliklarni inyeksiya qilish](guide/di/hierarchical-dependency-injection) - Injector ierarxiyasi qanday ishlaydi
- [Bogʻliqliklarni inyeksiya qilish bilan testlash](guide/testing) - TestBed'dan foydalanish va bogʻliqliklarni mock qilish
