# Reference: Skill Name

Detailed reference documentation for the skill.

## Format Specification

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| field_one | string | Description of field one |
| field_two | number | Description of field two |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| optional_one | boolean | false | Description |
| optional_two | string | "" | Description |

## API Reference

### Function One

```
functionOne(param1, param2)
```

**Parameters:**
- `param1` (required): Description
- `param2` (optional): Description

**Returns:** Description of return value

**Example:**
```
functionOne("value", 42)
```

### Function Two

```
functionTwo(options)
```

**Parameters:**
- `options.key1`: Description
- `options.key2`: Description

**Returns:** Description of return value

## Configuration Options

### Option Category One

```yaml
option_one: value
option_two: value
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| option_one | string | "default" | What it does |
| option_two | number | 10 | What it does |

### Option Category Two

```yaml
category:
  nested_option: value
```

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| ERR_001 | Description | How to fix |
| ERR_002 | Description | How to fix |

## Compatibility

| Version | Status | Notes |
|---------|--------|-------|
| 1.0 | Supported | Full support |
| 0.9 | Deprecated | Upgrade recommended |
