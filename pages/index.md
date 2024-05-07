---
title: Redfin Real Estate Report
---


```sql states
  select
      state
  from median_sale_price_per_state
  group by state
```

<Dropdown
    name=state
    data={states}
    value=state
    title="Select a State"
>
    <DropdownOption value="United States"/>
</Dropdown>


```sql property_types
  select
      property_type
  from median_sale_price_per_state
  group by property_type 
```


<ButtonGroup
    data={property_types} 
    name=Property_Types
    value=property_type
    title="Select a Property Type"
>
    <!-- <ButtonGroupItem valueLabel="All Categories" value="%" default /> -->
    <!-- <ButtonGroupItem valueLabel=Townhouse default /> -->
</ButtonGroup>


```sql median_sale_price_by_state
    SELECT * FROM median_sale_price_per_state
    WHERE state in(
        '${inputs.state.value}')
    AND property_type like '${inputs.Property_Types}'
```


<LineChart data={median_sale_price_by_state} x=period_end y=median_sale_price yAxisTitle="Median Sale Price">
    <ReferenceLine x='2020-03-11' label="Start Pandemic" hideValue=true/>
    <ReferenceLine x='2023-05-05' label="EnD Covid Pandemic" hideValue=true/>
</LineChart>


<!-- <LineChart 
    data={median_sale_price_by_state
    }  
    x=period_end
    y=median_sale_price
    title="Median Sale Price Per State"
/> -->

```sql median_ppsf_per_state
    SELECT * FROM median_ppsf_per_state
    WHERE state in(
        '${inputs.state.value}')
    AND property_type like '${inputs.Property_Types}'
```

<LineChart 
    data={median_ppsf_per_state
    }  
    x=period_end
    y=median_ppsf
    title="Median PPSF Per State"
/>


```sql homes_sold_per_state
    SELECT * FROM homes_sold_per_state
    WHERE state in(
        '${inputs.state.value}')
    AND property_type like '${inputs.Property_Types}'
```

<LineChart 
    data={homes_sold_per_state
    }  
    x=period_end
    y=homes_sold
    title="Homes Sold Per State"
/>

```sql scatter_chart
SELECT * FROM combined_price_homes_sold
WHERE property_type like '${inputs.Property_Types}'
AND state not in('United States', 'Columbia')
```

<ScatterPlot 
    data={scatter_chart} 
    x=median_sale_price
    y=homes_sold
    series=state 
    xAxisTitle=true 
    yAxisTitle=true
/>

```sql map
SELECT * FROM combined_price_homes_sold
WHERE property_type like '${inputs.Property_Types}'
```

<USMap
    data={map}
    state=state
    value=median_sale_price
    colorScale=bluegreen
    title="Median PPSF Map"
/>