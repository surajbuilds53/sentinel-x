"""Data loader for ingesting network flow CSV datasets."""

from pathlib import Path
from typing import List, Union, Optional
import logging
import pandas as pd

from sentinel_x.data.cleaner import clean_flow_dataframe

logger = logging.getLogger(__name__)


def load_single_csv(filepath: Union[str, Path], nrows: Optional[int] = None) -> pd.DataFrame:
    """Load a single CSV file with encoding fallback and basic verification.
    
    Args:
        filepath: Path to the CSV file.
        nrows: Optional limit on rows to read.
        
    Returns:
        pd.DataFrame containing loaded flow data.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Dataset file not found at: {path}")
        
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            df = pd.read_csv(path, nrows=nrows, encoding=enc, low_memory=False)
            logger.info(f"Successfully loaded {len(df)} rows from {path.name} (encoding={enc})")
            return df
        except UnicodeDecodeError:
            continue
            
    raise ValueError(f"Failed to decode CSV {path} with encodings: {encodings}")


def load_dataset(
    source: Union[str, Path, List[Union[str, Path]]],
    clean: bool = True,
    nrows: Optional[int] = None
) -> pd.DataFrame:
    """Load dataset from a file path, directory of CSVs, or list of file paths.
    
    Args:
        source: File path, directory path, or list of file paths.
        clean: If True, executes the cleaning pipeline.
        nrows: Optional limit on total rows to load.
        
    Returns:
        pd.DataFrame containing (optionally cleaned) flow records.
    """
    dfs: List[pd.DataFrame] = []
    
    if isinstance(source, (str, Path)):
        p = Path(source)
        if p.is_dir():
            files = sorted(list(p.glob("*.csv")))
            if not files:
                raise FileNotFoundError(f"No CSV files found in directory: {p}")
        elif p.is_file():
            files = [p]
        else:
            raise FileNotFoundError(f"Source path does not exist: {p}")
    elif isinstance(source, list):
        files = [Path(f) for f in source]
    else:
        raise TypeError(f"Unsupported source type: {type(source)}")
        
    for f in files:
        df = load_single_csv(f, nrows=nrows)
        dfs.append(df)
        if nrows and sum(len(x) for x in dfs) >= nrows:
            break
            
    combined = pd.concat(dfs, ignore_index=True)
    if nrows and len(combined) > nrows:
        combined = combined.iloc[:nrows]
        
    if clean:
        combined = clean_flow_dataframe(combined)
        
    return combined
