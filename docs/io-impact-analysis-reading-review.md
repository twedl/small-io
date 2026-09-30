# IO impact analysis: reading review

Sep 30, 2026 · @jesse

## Bottom line

Read chapter 20 of the UN *Handbook on Supply and Use Tables and Input-Output Tables* (2018) first. It is the best free overview of impact analysis for tables shaped like ours.

Our data is StatCan's symmetric (industry × industry) IO tables: national (catalogue 15-207-X) and provincial (15-211-X). The question is how to push a final-demand shock through them and read the result.

## Primary: UN Handbook, chapter 20

[*Handbook on Supply and Use Tables and Input-Output Tables with Extensions and Applications*](https://unstats.un.org/unsd/nationalaccount/docs/SUT_IOT_HB_Final_Cover.pdf) (UN, 2018), chapter 20, "Modelling applications of IOTs", pp. 603–640. It's free.

It fits our data because its worked table separates domestic products from imports, with imports as one row. That is how StatCan's `DomesticUse` sheets are laid out. One small numerical example runs through the whole chapter.

| Section | Page | What it gives us |
| --- | --- | --- |
| D. Input coefficients | 609 | A = Z / x on domestic flows |
| F. Quantity model | 612 | Leontief inverse: final-demand shock → output by industry |
| G. Price model | 616 | Cost-push effects, e.g. a tax or wage change |
| K. Multipliers | 629 | Type I vs Type II (induced) multipliers, Box 20.4 |
| L. Inter-industrial linkages | 636 | Backward and forward linkages |

In the same handbook, chapter 16 section C (p. 504) is Statistics Canada describing how it builds the provincial and territorial tables. It's useful background on our ground-truth data.

## Supplements

Two more sources fill gaps the UN chapter leaves: regional modelling in depth, and plain-language Canadian caveats.

| Source | Access | Read it for |
| --- | --- | --- |
| [Miller & Blair, *Input-Output Analysis: Foundations and Extensions*](https://www.cambridge.org/core/books/inputoutput-analysis/multipliers-in-the-inputoutput-model/D43C74DA2E76337272433A137FEACCA8) (Cambridge, 2022) | Paid | The standard textbook. Ch. 2 foundations, [ch. 3 regional models](https://cambridge.org/core/books/inputoutput-analysis/inputoutput-models-at-the-regional-level/7C59FB4BB52847747016C73E1909A45E), ch. 6 multipliers (pp. 238–288), chs. 9–10 nonsurvey methods (location quotients) |
| [NWT Bureau of Statistics, "NWT Input-Output Model – An Overview"](https://www.statsnwt.ca/economy/multipliers/NWT%20IO%20Model-Overview.pdf) (June 2006, 11 pages) | Free | Limitations: fixed coefficients, no capacity constraints, a 3–4 year data lag. Also the case against multipliers that include household spending (induced effects), e.g. fly-in/fly-out workers' income doesn't stay local. StatCan didn't publish induced multipliers in 2006; it does now |

The NWT overview describes StatCan's older commodity × industry model, not symmetric tables. Read it for the caveats, not the math.

## Caveat: StatCan's own multipliers

StatCan's published multipliers are derived from the supply and use tables, not from the symmetric tables we have. Use them as a sanity check on our Leontief results, not as an exact target.

- **What they cover.** The provincial and territorial multipliers ([36-10-0595-01](https://www150.statcan.gc.ca/n1/en/catalogue/3610059501)) show direct, indirect and induced effects on gross output, GDP components, jobs and imports, at Detail level.
- **How they're built.** The model documentation (a user's guide and "The Canadian and Inter-Provincial Input-Output Models: The Mathematical Framework") is [available only on request](https://www.statcan.gc.ca/en/subjects-start/economic_accounts/faq).
- **Custom runs.** StatCan runs its national (36-23-0001) and interprovincial (36-23-0002) models for clients on a cost-recovery basis.

## Sources

- [UN Handbook on Supply and Use Tables and Input-Output Tables (PDF, 2018)](https://unstats.un.org/unsd/nationalaccount/docs/SUT_IOT_HB_Final_Cover.pdf)
- [Miller & Blair, ch. 6: Multipliers in the Input–Output Model](https://www.cambridge.org/core/books/inputoutput-analysis/multipliers-in-the-inputoutput-model/D43C74DA2E76337272433A137FEACCA8)
- [NWT Bureau of Statistics, NWT Input-Output Model – An Overview (PDF, 2006)](https://www.statsnwt.ca/economy/multipliers/NWT%20IO%20Model-Overview.pdf)
- [StatCan table 36-10-0595-01: Input-output multipliers, provincial and territorial, detail level](https://www150.statcan.gc.ca/n1/en/catalogue/3610059501)
- [StatCan input-output accounts FAQ](https://www.statcan.gc.ca/en/subjects-start/economic_accounts/faq)
