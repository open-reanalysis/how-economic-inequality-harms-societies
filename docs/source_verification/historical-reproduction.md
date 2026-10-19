# Historical state source layout

Verified on 19 October 2026 before the first state correlation. Census’s historical state income page links its S4 table to state4.csv. The header begins with State; column 1 is household Gini for 1999, while later columns include different years and family Ginis. National totals and DC are explicitly excluded from the 50-state sample. Parsing stops at the SOURCE footer.

The FBI 1999 landing page links table5_state99.xls. Its Table5 worksheet has a header at zero-based row 3 and homicide at column 6. Uppercase state headings can carry trailing numeric footnote markers. The relevant row is the state rate per 100,000 inhabitants, following State Total. DC and Puerto Rico are outside the original 50-state sample. The reader preserves missing/suppressed source cells and does not derive rates from a different population denominator.

Both files were obtained through public federal download links with no registration or acceptance performed. Their response identities are in the acquisition records. Reader fixtures cover column selection and the handling of footnote-marked state headers.

## Census infant mortality recovery

The official Statistical Abstract 2006 vital-statistics page links Table 105 to https://www2.census.gov/library/publications/2005/compendia/statab/125ed/tables/06s0105.xlw. The authors' source notes name this table and the 2002 observation period. The workbook has a single 06s0105 sheet; year row 10, total-race column E, state rows 14–64 including DC. Footnote B denotes unreliable small-base data and remains null. The prospective historical specification was raised to version 3 before computing its comparison.
